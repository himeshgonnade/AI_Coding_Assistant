"""
Optimizer module — shows optimized alternative with AI chatbot explaining the difference.
Layout: Left column (User Code top + Optimized Code bottom) | Right column (AI Chatbot).
"""
import streamlit as st
from utils.groq_client import call_groq, call_groq_stream
from utils.styles import (
    module_header_html, section_title_html,
    panel_header_html, complexity_meter_html,
)

SYSTEM_PROMPT_ANALYZE = """You are LogicAI's Complexity Optimizer. Your job:
- Analyse user's code for time/space complexity
- Show 1-2 optimised alternatives
- NEVER say "yours is wrong" — say "yours works, here's what changes at scale"
- Be encouraging and educational

Format your response as EXACTLY this JSON:
{
  "user_approach": {
    "description": "Brief description of what the user's code does",
    "time_complexity": "O(...)",
    "space_complexity": "O(...)",
    "complexity_score": 70,
    "readability": "High/Medium/Low",
    "works_well_for": "small/medium/large inputs",
    "strength": "One strength of this approach"
  },
  "optimized": {
    "approach_name": "Name of the optimised technique",
    "description": "What the optimised approach does",
    "time_complexity": "O(...)",
    "space_complexity": "O(...)",
    "complexity_score": 20,
    "readability": "High/Medium/Low",
    "works_well_for": "large inputs",
    "key_insight": "The key insight that makes this faster",
    "when_to_use": "When this optimisation matters",
    "optimized_code": "The full optimised code as a string"
  },
  "scale_comparison": [
    {"input_size": "100 items",       "user_time": "~0.01ms",  "optimized_time": "~0.001ms"},
    {"input_size": "10,000 items",    "user_time": "~100ms",   "optimized_time": "~1ms"},
    {"input_size": "1,000,000 items", "user_time": "~Hours",   "optimized_time": "~100ms"}
  ],
  "encouragement": "A short, genuine encouraging sentence"
}
Return ONLY the JSON, no extra text."""

SYSTEM_PROMPT_CHAT = """You are LogicAI's Optimisation Tutor. The user is comparing their original code
with an AI-suggested optimised version. Your job:
- Help the user UNDERSTAND the difference between the two approaches
- Explain the data structure or algorithm insight that makes the optimised version faster
- Never just write code — explain concepts and reasoning
- Be concise, use markdown formatting, 3–5 sentences per response."""

COMPLEXITY_PCT = {
    "O(1)": 4, "O(log n)": 10, "O(n)": 22, "O(n log n)": 38,
    "O(n²)": 72, "O(n³)": 88, "O(2^n)": 97, "O(n!)": 100,
}


def _cpx_to_pct(tc: str) -> int:
    for k, v in COMPLEXITY_PCT.items():
        if k in tc:
            return v
    return 50


def render():
    st.markdown(
        module_header_html(
            "⚡", "Complexity Optimizer",
            "See what changes at scale — your code works, here's what improves"
        ),
        unsafe_allow_html=True,
    )

    # ── State init ────────────────────────────────────────────────────────────
    for key, default in [
        ("opt_result",       None),
        ("opt_chat_history", []),
    ]:
        if key not in st.session_state:
            st.session_state[key] = default

    # ── Auto-sync from editor ─────────────────────────────────────────────────
    synced = st.session_state.pop("opt_synced_code", None)
    if synced:
        st.session_state["_opt_prefill"] = synced
        st.session_state.opt_result      = None

    prefill = st.session_state.get("_opt_prefill", "")
    current_code = (
        st.session_state.get("editor_code", "")
        or prefill
        or ""
    )

    # ── MAIN LAYOUT ───────────────────────────────────────────────────────────
    col_left, col_right = st.columns([1, 1])

    # ══════════════════════════════════════════════════════════════════════════
    # LEFT COLUMN — User Code (top) + Optimized Code (bottom)
    # ══════════════════════════════════════════════════════════════════════════
    with col_left:
        # ── User Code ─────────────────────────────────────────────────────────
        st.markdown(
            panel_header_html("📝", "Your Code"),
            unsafe_allow_html=True,
        )

        if prefill:
            st.markdown(
                """
<div class="info-box tip" style="margin:6px 0;">
    <span>📎</span>
    <span><strong>Editor code synced!</strong> Ready to optimise.</span>
</div>
""",
                unsafe_allow_html=True,
            )

        user_code_display = current_code or "# Write your code in the editor first"
        st.code(
            user_code_display,
            language=st.session_state.get("editor_language", "python"),
        )

        # User approach analysis (if available)
        if st.session_state.opt_result:
            ua = st.session_state.opt_result.get("user_approach", {})
            tc  = ua.get("time_complexity", "O(?)")
            pct = _cpx_to_pct(tc)
            st.markdown(
                f"""
<div class="glass-card" style="margin-top:8px;">
    <h3 style="color:#f59e0b;">📊 Your Approach</h3>
    <div style="font-size:12px;color:#94a3b8;margin-bottom:10px;line-height:1.6;">
        {ua.get('description','')}
    </div>
""",
                unsafe_allow_html=True,
            )
            st.markdown(
                complexity_meter_html("⏱ Time", tc, pct, danger=pct > 40),
                unsafe_allow_html=True,
            )
            st.markdown(
                f"""
    <div style="font-size:12px;margin:8px 0;">
        <div class="complexity-row">
            <span class="complexity-label">Space</span>
            <span class="complexity-value">{ua.get('space_complexity','O(?)')}</span>
        </div>
        <div class="complexity-row">
            <span class="complexity-label">Readability</span>
            <span class="complexity-value">{ua.get('readability','-')}</span>
        </div>
        <div class="complexity-row">
            <span class="complexity-label">Good for</span>
            <span class="complexity-value">{ua.get('works_well_for','-')}</span>
        </div>
    </div>
    <div style="font-size:12px;color:#10b981;">✅ {ua.get('strength','')}</div>
</div>
""",
                unsafe_allow_html=True,
            )

        # ── Optimized Code ────────────────────────────────────────────────────
        st.markdown(
            '<div style="height:8px;background:rgba(139,92,246,0.15);border-radius:4px;margin:12px 0;"></div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            panel_header_html("🚀", "Optimized Code"),
            unsafe_allow_html=True,
        )

        if st.session_state.opt_result:
            op = st.session_state.opt_result.get("optimized", {})
            opt_code = op.get("optimized_code", "# Optimised code will appear here after analysis")
            tc2  = op.get("time_complexity", "O(?)")
            pct2 = _cpx_to_pct(tc2)

            st.code(
                opt_code,
                language=st.session_state.get("editor_language", "python"),
            )

            st.markdown(
                f"""
<div class="glass-card" style="border-color:rgba(139,92,246,0.35);">
    <h3 style="color:#8b5cf6;">🚀 {op.get('approach_name','Optimised Approach')}</h3>
    <div style="font-size:12px;color:#94a3b8;margin-bottom:10px;line-height:1.6;">
        {op.get('description','')}
    </div>
""",
                unsafe_allow_html=True,
            )
            st.markdown(
                complexity_meter_html("⏱ Time", tc2, pct2, danger=False),
                unsafe_allow_html=True,
            )
            st.markdown(
                f"""
    <div style="font-size:12px;margin:8px 0;">
        <div class="complexity-row">
            <span class="complexity-label">Space</span>
            <span class="complexity-value">{op.get('space_complexity','O(?)')}</span>
        </div>
        <div class="complexity-row">
            <span class="complexity-label">Key Insight</span>
            <span class="complexity-value" style="color:#06b6d4;">💡</span>
        </div>
    </div>
    <div style="font-size:12px;color:#06b6d4;line-height:1.6;">{op.get('key_insight','')}</div>
</div>
""",
                unsafe_allow_html=True,
            )

            # Scale comparison
            scale = st.session_state.opt_result.get("scale_comparison", [])
            if scale:
                st.markdown(section_title_html("PERFORMANCE AT SCALE"), unsafe_allow_html=True)
                rows = "".join(
                    f"""<tr>
<td><strong>{r.get('input_size','')}</strong></td>
<td style="color:#f59e0b;">{r.get('user_time','')}</td>
<td style="color:#10b981;">{r.get('optimized_time','')}</td>
</tr>"""
                    for r in scale
                )
                st.markdown(
                    f"""
<div class="glass-card" style="overflow-x:auto;padding:12px;">
    <table class="var-table" style="width:100%;">
        <thead>
            <tr>
                <th>Input Size</th>
                <th style="color:#f59e0b;">📝 Your Approach</th>
                <th style="color:#10b981;">🚀 Optimised</th>
            </tr>
        </thead>
        <tbody>{rows}</tbody>
    </table>
</div>
""",
                    unsafe_allow_html=True,
                )
        else:
            # Empty state for optimized code
            btn_c1, btn_c2 = st.columns([3, 1])
            with btn_c1:
                if st.button(
                    "⚡ Analyse & Optimise",
                    key="opt_analyse_btn",
                    use_container_width=True,
                    type="primary",
                ):
                    if current_code.strip():
                        with st.spinner("⚡ Analysing complexity…"):
                            import json
                            raw = call_groq(
                                SYSTEM_PROMPT_ANALYZE,
                                f"Analyse this code:\n\n```\n{current_code}\n```",
                            )
                            try:
                                cleaned = raw.strip()
                                if cleaned.startswith("```"):
                                    cleaned = cleaned.split("```")[1]
                                    if cleaned.startswith("json"):
                                        cleaned = cleaned[4:]
                                st.session_state.opt_result = json.loads(cleaned)
                                # Pre-seed the chatbot
                                enc = st.session_state.opt_result.get("encouragement", "")
                                if enc:
                                    st.session_state.opt_chat_history = [
                                        {"role": "ai", "content": f"✅ **{enc}**\n\nAsk me anything about the difference between your approach and the optimised one!"}
                                    ]
                                st.rerun()
                            except Exception as e:
                                st.error(f"Parse error: {e}")
                    else:
                        st.warning("Write code in the editor first.")
            with btn_c2:
                if st.button("🗑️ Clear", key="opt_clear_btn", use_container_width=True):
                    st.session_state.opt_result = None
                    st.session_state.opt_chat_history = []
                    st.rerun()

            st.markdown(
                """
<div style="text-align:center;padding:40px 0;color:#475569;">
    <div style="font-size:48px;margin-bottom:12px;
        filter:drop-shadow(0 0 16px rgba(139,92,246,0.4));">⚡</div>
    <div style="font-size:14px;font-weight:600;color:#94a3b8;margin-bottom:6px;">
        No analysis yet
    </div>
    <div style="font-size:12px;">
        Click <strong>Analyse & Optimise</strong> to see the optimised version
    </div>
</div>
""",
                unsafe_allow_html=True,
            )

    # ══════════════════════════════════════════════════════════════════════════
    # RIGHT COLUMN — AI Chatbot
    # ══════════════════════════════════════════════════════════════════════════
    with col_right:
        st.markdown(
            panel_header_html("🧠", "AI Optimisation Tutor"),
            unsafe_allow_html=True,
        )
        st.markdown(
            """
<div style="padding:8px 14px 4px;font-size:11px;color:#475569;
    border-bottom:1px solid rgba(139,92,246,0.08);">
    💡 I help you <em>understand</em> the difference — not just copy the optimised code.
</div>
""",
            unsafe_allow_html=True,
        )

        # Chat history
        chat_html = ""
        for msg in st.session_state.opt_chat_history[-14:]:
            if msg["role"] == "user":
                safe = msg["content"].replace("<", "&lt;").replace(">", "&gt;")
                chat_html += f'<div class="chat-bubble-user">{safe}</div>'
            else:
                safe = msg["content"].replace("<", "&lt;").replace(">", "&gt;")
                chat_html += f"""
<div class="chat-bubble-ai">
    <div class="ai-label">🧠 LogicAI</div>
    {safe}
</div>"""

        if not chat_html:
            chat_html = """
<div style='color:#475569;font-size:12px;text-align:center;padding:40px 10px;'>
    <div style='font-size:36px;margin-bottom:10px;
        filter:drop-shadow(0 0 14px rgba(139,92,246,0.4))'>⚡</div>
    <div style='color:#94a3b8;font-weight:600;margin-bottom:6px;'>Optimisation Tutor</div>
    After analysis, ask me:<br>
    <em>"Why is a hash map faster here?"</em><br>
    <em>"When does O(n²) matter?"</em><br>
    <em>"What's the trade-off?"</em>
</div>"""

        st.markdown(
            f'<div class="chat-scroll" style="max-height:420px;">{chat_html}</div>',
            unsafe_allow_html=True,
        )

        # Chat input form
        with st.form("opt_chat_form", clear_on_submit=True):
            c_in, c_btn = st.columns([5, 1])
            with c_in:
                opt_msg = st.text_input(
                    "opt_chat_input",
                    placeholder="Ask about the optimisation difference…",
                    label_visibility="collapsed",
                    key="opt_msg_field",
                )
            with c_btn:
                opt_send = st.form_submit_button("➤", use_container_width=True)

        if opt_send and opt_msg.strip():
            st.session_state.opt_chat_history.append(
                {"role": "user", "content": opt_msg}
            )
            _context = ""
            if st.session_state.opt_result:
                ua = st.session_state.opt_result.get("user_approach", {})
                op = st.session_state.opt_result.get("optimized", {})
                _context = (
                    f"User's original code:\n```\n{current_code}\n```\n\n"
                    f"User approach: {ua.get('time_complexity','')} — {ua.get('description','')}\n"
                    f"Optimised approach ({op.get('approach_name','')}): "
                    f"{op.get('time_complexity','')} — {op.get('description','')}\n"
                    f"Key insight: {op.get('key_insight','')}"
                )
            _prompt = f"{_context}\n\nUser question: {opt_msg}"
            with st.spinner("🧠 Thinking…"):
                full_resp = ""
                for chunk in call_groq_stream(SYSTEM_PROMPT_CHAT, _prompt):
                    full_resp += chunk
            st.session_state.opt_chat_history.append(
                {"role": "ai", "content": full_resp}
            )
            st.rerun()

        # Analyse button (also available on right side for convenience)
        if not st.session_state.opt_result:
            st.markdown('<div style="margin-top:12px;"></div>', unsafe_allow_html=True)
            if st.button(
                "⚡ Analyse Code Now",
                key="opt_analyse_right",
                use_container_width=True,
                type="primary",
            ):
                if current_code.strip():
                    with st.spinner("⚡ Analysing…"):
                        import json
                        raw = call_groq(
                            SYSTEM_PROMPT_ANALYZE,
                            f"Analyse this code:\n\n```\n{current_code}\n```",
                        )
                        try:
                            cleaned = raw.strip()
                            if cleaned.startswith("```"):
                                cleaned = cleaned.split("```")[1]
                                if cleaned.startswith("json"):
                                    cleaned = cleaned[4:]
                            st.session_state.opt_result = json.loads(cleaned)
                            enc = st.session_state.opt_result.get("encouragement", "")
                            if enc:
                                st.session_state.opt_chat_history = [
                                    {"role": "ai",
                                     "content": f"✅ **{enc}**\n\nAsk me about the difference between your approach and the optimised one!"}
                                ]
                            st.rerun()
                        except Exception as e:
                            st.error(f"Parse error: {e}")
                else:
                    st.warning("Write code in the editor first.")
        else:
            # Clear button in right panel too
            if st.button("🔄 Reset Analysis", key="opt_reset_right", use_container_width=True):
                st.session_state.opt_result = None
                st.session_state.opt_chat_history = []
                st.rerun()
