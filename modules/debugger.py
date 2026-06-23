"""
Debugger module — Socratic step-by-step debugging partner.
Layout: Left = read-only code mirror | Right = debugger interface.
"""
import streamlit as st
from utils.groq_client import call_groq, call_groq_stream
from utils.styles import module_header_html, section_title_html, panel_header_html

SYSTEM_PROMPT_INIT = """You are LogicAI's Socratic Debugging Partner. STRICT rules:
1. NEVER fix the bug for the user.
2. NEVER show corrected code.
3. Guide them to find it themselves through Socratic questions.
4. Use the method: ask what they expect → what they observe → notice the difference.

When user shares broken code + error, respond with EXACTLY this JSON:
{
  "initial_observation": "What you notice about the code (without revealing the bug)",
  "first_question": "Your first Socratic question to get them thinking",
  "hint_print_statement": "A print/console.log statement they should add to investigate",
  "bug_category": "Type of bug: off-by-one / type error / logic error / scope error / etc."
}
Return ONLY valid JSON."""

SYSTEM_PROMPT_FOLLOWUP = """You are LogicAI's Socratic Debugging Partner. NEVER give the answer directly.
Continue the Socratic method:
- Getting closer → acknowledge and push deeper with a follow-up question
- Found it → congratulate and explain WHY this bug happens
- Stuck → give a slightly more direct hint, still as a question
Always end with a question or learning insight. Use markdown formatting."""


def render():
    st.markdown(
        module_header_html("🐛", "Guided Debugging Partner",
                           "I walk you through finding the bug — not fixing it for you"),
        unsafe_allow_html=True,
    )

    # ── Session state init ────────────────────────────────────────────────────
    for key, default in [
        ("debug_history", []),
        ("debug_session_started", False),
        ("debug_bug_category", ""),
        ("debug_hint", ""),
    ]:
        if key not in st.session_state:
            st.session_state[key] = default

    # ── Auto-sync from editor ─────────────────────────────────────────────────
    synced = st.session_state.pop("debug_synced_code", None)
    if synced and not st.session_state.debug_session_started:
        st.session_state["_debug_prefill"] = synced

    prefill = st.session_state.get("_debug_prefill", "")

    # ── Two-column layout ─────────────────────────────────────────────────────
    col_code, col_debug = st.columns([1, 1])

    # ── LEFT: Code Mirror ─────────────────────────────────────────────────────
    with col_code:
        st.markdown(
            panel_header_html("💻", "Your Code"),
            unsafe_allow_html=True,
        )

        current_code = (
            st.session_state.get("editor_code", "")
            or prefill
            or "# No code in editor yet."
        )

        # Show the live editor code (read-only display)
        st.markdown(section_title_html("CODE FROM EDITOR"), unsafe_allow_html=True)
        st.code(current_code, language=st.session_state.get("editor_language", "python"))

        # Philosophy box
        st.markdown(
            """
<div class="info-box philosophy" style="margin-top:12px;">
    <span>🔍</span>
    <span>I won't fix your bug. Instead, I'll ask the right questions
    until <em>you</em> find it — building a debugging mindset that lasts.</span>
</div>
""",
            unsafe_allow_html=True,
        )

    # ── RIGHT: Debugger Interface ─────────────────────────────────────────────
    with col_debug:
        st.markdown(
            panel_header_html("🐛", "Debug Session"),
            unsafe_allow_html=True,
        )

        if not st.session_state.debug_session_started:
            # ── START SCREEN ─────────────────────────────────────────────────
            if prefill:
                st.markdown(
                    """
<div class="info-box tip">
    <span>📎</span>
    <span><strong>Editor code synced!</strong> Describe the error below to start.</span>
</div>
""",
                    unsafe_allow_html=True,
                )

            st.markdown(section_title_html("BROKEN CODE"), unsafe_allow_html=True)
            broken_code = st.text_area(
                "Broken code",
                value=prefill or current_code,
                placeholder="# Paste your broken code here...",
                height=220,
                label_visibility="collapsed",
                key="debug_code_input",
            )

            st.markdown(section_title_html("ERROR / UNEXPECTED OUTPUT"), unsafe_allow_html=True)
            error_msg = st.text_area(
                "Error",
                placeholder="Paste the error message OR describe unexpected behavior…",
                height=90,
                label_visibility="collapsed",
                key="debug_error_input",
            )

            if st.button("🐛 Start Debug Session", use_container_width=True, key="start_debug"):
                if broken_code.strip() and error_msg.strip():
                    prompt = (
                        f"Broken code:\n```\n{broken_code}\n```\n\nError/problem: {error_msg}"
                    )
                    with st.spinner("🔍 Analysing without giving away the answer…"):
                        import json
                        raw = call_groq(SYSTEM_PROMPT_INIT, prompt)
                        try:
                            cleaned = raw.strip()
                            if cleaned.startswith("```"):
                                cleaned = cleaned.split("```")[1]
                                if cleaned.startswith("json"):
                                    cleaned = cleaned[4:]
                            data = json.loads(cleaned)
                            first_q   = data.get("first_question", "What do you think is happening?")
                            hint_p    = data.get("hint_print_statement", "")
                            obs       = data.get("initial_observation", "")
                            st.session_state.debug_bug_category = data.get("bug_category", "")
                            st.session_state.debug_hint = hint_p

                            opening = f"{obs}\n\n**{first_q}**"
                            if hint_p:
                                opening += f"\n\n*Try adding this to investigate:*\n```python\n{hint_p}\n```"

                            st.session_state.debug_history = [
                                {"role": "context",
                                 "content": f"**Code:**\n```\n{broken_code}\n```\n\n**Error:** {error_msg}"},
                                {"role": "assistant", "content": opening},
                            ]
                            st.session_state.debug_session_started = True
                            st.rerun()
                        except Exception as e:
                            st.session_state.debug_history = [
                                {"role": "context",
                                 "content": f"**Code:**\n```\n{broken_code}\n```\n\n**Error:** {error_msg}"},
                                {"role": "assistant", "content": raw},
                            ]
                            st.session_state.debug_session_started = True
                            st.rerun()
                else:
                    st.warning("Please provide both broken code and the error message.")

        else:
            # ── ACTIVE DEBUG SESSION ──────────────────────────────────────────
            header_c, reset_c = st.columns([5, 1])
            with reset_c:
                if st.button("🔄 New", key="debug_reset", use_container_width=True):
                    st.session_state.debug_session_started = False
                    st.session_state.debug_history = []
                    st.session_state.debug_bug_category = ""
                    st.rerun()

            # Bug category badge
            if st.session_state.debug_bug_category:
                st.markdown(
                    f"""
<div style="margin-bottom:10px;">
    <span class="badge badge-amber">🏷️ {st.session_state.debug_bug_category}</span>
</div>
""",
                    unsafe_allow_html=True,
                )

            # Progress steps
            hist_len = len(st.session_state.debug_history)
            steps = [
                ("❌", "Error shown",       True),
                ("🤔", "Expectations?",     hist_len > 2),
                ("🔍", "Add print/log",     hist_len > 4),
                ("💡", "Notice difference", hist_len > 6),
                ("✅", "Bug found!",        hist_len > 8),
            ]
            step_html = "".join(
                f"""
<div style="text-align:center;flex:1;">
    <div style="font-size:18px;margin-bottom:3px;">{icon}</div>
    <div style="font-size:10px;color:{'#94a3b8' if done else '#374151'};line-height:1.3;">{label}</div>
    <div style="height:3px;margin-top:5px;border-radius:2px;
        background:{'linear-gradient(90deg,#8b5cf6,#06b6d4)' if done else 'rgba(255,255,255,0.05)'};"></div>
</div>
"""
                for icon, label, done in steps
            )
            st.markdown(
                f'<div style="display:flex;gap:4px;margin-bottom:14px;">{step_html}</div>',
                unsafe_allow_html=True,
            )

            # Debug history
            st.markdown(section_title_html("DEBUG SESSION"), unsafe_allow_html=True)
            chat_area = st.container()
            with chat_area:
                for msg in st.session_state.debug_history:
                    if msg["role"] == "context":
                        with st.expander("📄 View Original Code & Error", expanded=False):
                            st.markdown(msg["content"])
                    elif msg["role"] == "assistant":
                        st.markdown(
                            f"""
<div class="debug-question">
    <div class="q-label">🧠 LogicAI</div>
    {msg['content'].replace(chr(10), '<br>')}
</div>
""",
                            unsafe_allow_html=True,
                        )
                    elif msg["role"] == "user":
                        st.markdown(
                            f"""
<div class="user-message">
    <div class="user-label">👤 You</div>
    {msg['content'].replace('<','&lt;').replace('>','&gt;')}
</div>
""",
                            unsafe_allow_html=True,
                        )

            # User response
            st.markdown(section_title_html("YOUR RESPONSE"), unsafe_allow_html=True)
            with st.form("debug_respond_form", clear_on_submit=True):
                user_resp = st.text_area(
                    "Your response",
                    placeholder="What do you think? What did the print show? What did you expect vs observe?",
                    height=80,
                    label_visibility="collapsed",
                    key="debug_user_resp",
                )
                if st.form_submit_button("💬 Respond", use_container_width=True):
                    if user_resp.strip():
                        st.session_state.debug_history.append(
                            {"role": "user", "content": user_resp}
                        )
                        context = "\n".join(
                            f"{'LogicAI' if m['role']=='assistant' else 'Context' if m['role']=='context' else 'Student'}: {m['content']}"
                            for m in st.session_state.debug_history[-6:]
                        )
                        with st.spinner("🔍 Thinking Socratically…"):
                            full_resp = ""
                            for chunk in call_groq_stream(SYSTEM_PROMPT_FOLLOWUP, context):
                                full_resp += chunk
                        st.session_state.debug_history.append(
                            {"role": "assistant", "content": full_resp}
                        )
                        st.rerun()
