import streamlit as st
from utils.groq_client import call_groq
from utils.styles import module_header_html, section_title_html

SYSTEM_PROMPT_INIT = """You are LogicPilot's Socratic Debugging Partner. Your STRICT rules:
1. NEVER fix the bug for the user
2. NEVER show corrected code
3. Guide them to find it themselves through questions
4. Use the Socratic method: ask what they expect, then what they observe, then notice the difference

When user shares broken code + error, respond with EXACTLY this JSON:
{
  "initial_observation": "What you notice about the code (without revealing the bug)",
  "first_question": "Your first Socratic question to get them thinking",
  "hint_print_statement": "A print statement they should add to investigate (e.g., print(x))",
  "bug_category": "Type of bug: off-by-one / type error / logic error / scope error / etc."
}

Return ONLY valid JSON."""

SYSTEM_PROMPT_FOLLOWUP = """You are LogicPilot's Socratic Debugging Partner. NEVER give the answer directly.
The user is debugging their code. Continue the Socratic questioning:
- If they're getting closer: acknowledge and push deeper with a follow-up question
- If they found it: congratulate them and explain WHY this type of bug happens
- If they're stuck: give a slightly more direct hint but still as a question
- Always end with a question or a learning insight

Respond conversationally. You may use markdown formatting."""

def render():
    st.markdown(module_header_html(
        "🐛", "Guided Debugging Partner",
        "Paste broken code + error — I'll walk you through finding the bug yourself"
    ), unsafe_allow_html=True)

    st.markdown("""
    <div class="info-box philosophy">
        <span>🔍</span>
        <span>I won't fix your bug. Instead, I'll ask you the right questions until
        <em>you</em> find it. Finding bugs yourself builds a debugging mental model that lasts.</span>
    </div>
    """, unsafe_allow_html=True)

    # Init state
    if "debug_history" not in st.session_state:
        st.session_state.debug_history = []
    if "debug_session_started" not in st.session_state:
        st.session_state.debug_session_started = False
    if "debug_bug_category" not in st.session_state:
        st.session_state.debug_bug_category = ""
    if "debug_hint" not in st.session_state:
        st.session_state.debug_hint = ""

    # ── Auto-sync from editor ─────────────────────────────────────────────────
    synced_code = st.session_state.pop("debug_synced_code", None)
    if synced_code and not st.session_state.debug_session_started:
        st.session_state["_debug_prefill"] = synced_code

    prefill_code = st.session_state.get("_debug_prefill", "")

    if not st.session_state.debug_session_started:
        if prefill_code:
            st.markdown("""
            <div class="info-box tip" style="margin-bottom:12px;">
                <span>📎</span>
                <span><strong>Editor code synced!</strong> Your code is pre-loaded.
                Just describe the error or unexpected behavior below.</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown(section_title_html("BROKEN CODE"), unsafe_allow_html=True)

        broken_code = st.text_area(
            "Broken code",
            value=prefill_code if prefill_code else "",
            placeholder="# Paste your broken code here...\n\ndef calculate_average(nums):\n    total = 0\n    for n in nums:\n        total += n\n    return total / len(nums)",
            height=180,
            label_visibility="collapsed",
            key="debug_code"
        )
        if prefill_code:
            st.markdown("""
            <div style="font-size:11px; color:#6366f1; margin-top:-8px; margin-bottom:4px;">
                📎 Auto-filled from editor
            </div>
            """, unsafe_allow_html=True)

        st.markdown(section_title_html("ERROR / UNEXPECTED OUTPUT"), unsafe_allow_html=True)
        error_msg = st.text_area(
            "Error message",
            placeholder="Paste the error message OR describe the unexpected behavior...\ne.g. ZeroDivisionError: division by zero\nOR: It returns None instead of the sum",
            height=90,
            label_visibility="collapsed",
            key="debug_error"
        )

        if st.button("🐛 Start Debug Session", use_container_width=False):
            if broken_code.strip() and error_msg.strip():
                prompt = f"Broken code:\n```\n{broken_code}\n```\n\nError/problem: {error_msg}"
                with st.spinner("🔍 Analyzing without revealing the answer..."):
                    import json
                    raw = call_groq(SYSTEM_PROMPT_INIT, prompt)
                    try:
                        cleaned = raw.strip()
                        if cleaned.startswith("```"):
                            cleaned = cleaned.split("```")[1]
                            if cleaned.startswith("json"):
                                cleaned = cleaned[4:]
                        data = json.loads(cleaned)
                        first_q = data.get("first_question", "What do you think is happening on the first line that fails?")
                        hint_print = data.get("hint_print_statement", "")
                        observation = data.get("initial_observation", "")
                        st.session_state.debug_bug_category = data.get("bug_category", "")
                        st.session_state.debug_hint = hint_print

                        # Build opening message
                        opening = f"{observation}\n\n**{first_q}**"
                        if hint_print:
                            opening += f"\n\n*Try adding this to investigate:*\n```python\n{hint_print}\n```"

                        st.session_state.debug_history = [
                            {"role": "context", "content": f"**Code:**\n```\n{broken_code}\n```\n\n**Error:** {error_msg}"},
                            {"role": "assistant", "content": opening}
                        ]
                        st.session_state.debug_session_started = True
                        st.rerun()
                    except Exception as e:
                        st.error(f"Parse error: {e}")
                        st.session_state.debug_history = [
                            {"role": "context", "content": f"**Code:**\n```\n{broken_code}\n```\n\n**Error:** {error_msg}"},
                            {"role": "assistant", "content": raw}
                        ]
                        st.session_state.debug_session_started = True
                        st.rerun()

    else:
        # Active debug session
        col1, col2 = st.columns([4, 1])
        with col2:
            if st.button("🔄 New Bug", use_container_width=True):
                st.session_state.debug_session_started = False
                st.session_state.debug_history = []
                st.session_state.debug_bug_category = ""
                st.rerun()

        # Bug category badge
        if st.session_state.debug_bug_category:
            st.markdown(f"""
            <div style="margin-bottom:12px;">
                <span class="badge badge-amber">🏷️ Bug Category: {st.session_state.debug_bug_category}</span>
            </div>
            """, unsafe_allow_html=True)

        # Debugging flow steps visual
        flow_steps = [
            ("❌", "Error shown", True),
            ("🤔", "Your expectation?", len(st.session_state.debug_history) > 2),
            ("🔍", "Add print statement", len(st.session_state.debug_history) > 4),
            ("💡", "Notice the difference", len(st.session_state.debug_history) > 6),
            ("✅", "Bug found!", len(st.session_state.debug_history) > 8),
        ]

        cols = st.columns(5)
        for i, (icon, label, done) in enumerate(flow_steps):
            with cols[i]:
                color = "#10b981" if done else "#374151"
                st.markdown(f"""
                <div style="text-align:center; padding:8px 0;">
                    <div style="font-size:20px; margin-bottom:4px;">{icon}</div>
                    <div style="font-size:10px; color:{'#94a3b8' if done else '#4b5563'}; line-height:1.3;">
                        {label}
                    </div>
                    <div style="height:3px; background:{'var(--gradient-hero)' if done else 'rgba(255,255,255,0.05)'};
                        border-radius:2px; margin-top:6px;"></div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown(section_title_html("DEBUG SESSION"), unsafe_allow_html=True)

        # Display history
        for msg in st.session_state.debug_history:
            if msg["role"] == "context":
                with st.expander("📄 View Code & Error", expanded=False):
                    st.markdown(msg["content"])
            elif msg["role"] == "assistant":
                st.markdown(f"""
                <div class="debug-question">
                    <div class="q-label">🧠 LogicPilot</div>
                    {msg['content'].replace(chr(10), '<br>')}
                </div>
                """, unsafe_allow_html=True)
            elif msg["role"] == "user":
                st.markdown(f"""
                <div class="user-message">
                    <div class="user-label">👤 You</div>
                    {msg['content']}
                </div>
                """, unsafe_allow_html=True)

        # User response input
        st.markdown(section_title_html("YOUR ANSWER"), unsafe_allow_html=True)
        user_response = st.text_area(
            "Your debugging response",
            placeholder="What do you think? What did the print statement show? What did you expect vs what happened?",
            height=90,
            label_visibility="collapsed",
            key="debug_user_input"
        )

        col_a, col_b = st.columns([1, 4])
        with col_a:
            if st.button("💬 Respond", use_container_width=True, key="debug_send"):
                if user_response.strip():
                    st.session_state.debug_history.append({"role": "user", "content": user_response})

                    # Build context for follow-up
                    context = "\n".join([
                        f"{'LogicPilot' if m['role']=='assistant' else 'Context' if m['role']=='context' else 'Student'}: {m['content']}"
                        for m in st.session_state.debug_history[-6:]
                    ])

                    with st.spinner("🔍 Thinking Socratically..."):
                        full_resp = ""
                        for chunk in __import__('utils.groq_client', fromlist=['call_groq_stream']).call_groq_stream(
                            SYSTEM_PROMPT_FOLLOWUP, context
                        ):
                            full_resp += chunk

                    st.session_state.debug_history.append({"role": "assistant", "content": full_resp})
                    st.rerun()
