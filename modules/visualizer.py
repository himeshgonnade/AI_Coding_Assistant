import streamlit as st
from utils.groq_client import call_groq
from utils.styles import module_header_html, section_title_html

SYSTEM_PROMPT = """You are LogicPilot's Visual Code Explainer. Your job:
- Take a code snippet and simulate its execution step-by-step
- For each step, track variable states and what's happening
- Generate a visual "story" of what the computer is doing

Format EXACTLY as JSON:
{
  "language": "python",
  "summary": "One-line description of what this code does",
  "steps": [
    {
      "step": 1,
      "line": "exact line of code",
      "line_number": 1,
      "action": "What the computer is doing at this step",
      "variables": {"var1": "value1", "var2": "value2"},
      "changed_vars": ["var1"],
      "callstack": ["main"],
      "output": "any print output (empty string if none)",
      "highlight": "Key insight about this line"
    }
  ],
  "final_output": "The final result/return value",
  "key_patterns": ["pattern1", "pattern2"]
}

Be thorough — include EVERY significant operation. Show actual values, not placeholders.
Return ONLY valid JSON."""

def render():
    st.markdown(module_header_html(
        "🔬", "Visual Code Stepper",
        "Step through your code line by line — watch every variable change in slow motion"
    ), unsafe_allow_html=True)

    st.markdown("""
    <div class="info-box philosophy">
        <span>🎬</span>
        <span>Like a slow-motion replay of what the computer is doing.
        Watch variables change, loops iterate, and your logic unfold — one step at a time.</span>
    </div>
    """, unsafe_allow_html=True)

    if "vis_steps" not in st.session_state:
        st.session_state.vis_steps = []
    if "vis_current" not in st.session_state:
        st.session_state.vis_current = 0
    if "vis_summary" not in st.session_state:
        st.session_state.vis_summary = ""
    if "vis_patterns" not in st.session_state:
        st.session_state.vis_patterns = []

    # ── Auto-sync from editor ─────────────────────────────────────────────────
    synced_code = st.session_state.pop("vis_synced_code", None)
    if synced_code:
        st.session_state["_vis_prefill"] = synced_code
        st.session_state.vis_steps = []   # reset previous visualization
        st.session_state.vis_current = 0

    prefill_code = st.session_state.get("_vis_prefill", "")

    if prefill_code:
        st.markdown("""
        <div class="info-box tip" style="margin-bottom:12px;">
            <span>📎</span>
            <span><strong>Editor code synced!</strong> Your code is pre-loaded and ready to visualize step-by-step.</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(section_title_html("CODE TO VISUALIZE"), unsafe_allow_html=True)

    code_input = st.text_area(
        "Paste code",
        value=prefill_code if prefill_code else "",
        placeholder="# Paste a small function or snippet (keep it short for best results)\n\ndef factorial(n):\n    if n == 0:\n        return 1\n    return n * factorial(n-1)\n\nresult = factorial(4)",
        height=180,
        label_visibility="collapsed",
        key="vis_code"
    )
    if prefill_code:
        st.markdown("""
        <div style="font-size:11px; color:#6366f1; margin-top:-8px; margin-bottom:4px;">
            📎 Auto-filled from editor
        </div>
        """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1, 4])
    with col1:
        if st.button("🔬 Visualize!", use_container_width=True):
            if code_input.strip():
                with st.spinner("🔬 Simulating execution..."):
                    import json
                    raw = call_groq(SYSTEM_PROMPT, f"Visualize this code step by step:\n\n```\n{code_input}\n```")
                    try:
                        cleaned = raw.strip()
                        if cleaned.startswith("```"):
                            cleaned = cleaned.split("```")[1]
                            if cleaned.startswith("json"):
                                cleaned = cleaned[4:]
                        data = json.loads(cleaned)
                        st.session_state.vis_steps = data.get("steps", [])
                        st.session_state.vis_current = 0
                        st.session_state.vis_summary = data.get("summary", "")
                        st.session_state.vis_patterns = data.get("key_patterns", [])
                        st.rerun()
                    except Exception as e:
                        st.error(f"Parse error: {e}")
    with col2:
        if st.button("🗑️ Clear", use_container_width=False):
            st.session_state.vis_steps = []
            st.session_state.vis_current = 0
            st.rerun()

    if st.session_state.vis_steps:
        steps = st.session_state.vis_steps
        current = st.session_state.vis_current
        total = len(steps)
        step = steps[current]

        # Summary and progress
        st.markdown(f"""
        <div class="glass-card">
            <div style="font-size:12px; color:#94a3b8; margin-bottom:6px;">
                📝 <strong>Code does:</strong> {st.session_state.vis_summary}
            </div>
            <div style="font-size:12px; color:#64748b;">
                Step {current + 1} of {total}
            </div>
            <div class="progress-bar-wrap" style="margin-top:8px;">
                <div class="progress-bar-fill" style="width:{int(((current+1)/total)*100)}%"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Navigation controls
        nav_col1, nav_col2, nav_col3, nav_col4, nav_col5 = st.columns([1, 1, 2, 1, 1])
        with nav_col1:
            if st.button("⏮️", help="First step"):
                st.session_state.vis_current = 0
                st.rerun()
        with nav_col2:
            if st.button("◀️", help="Previous"):
                if current > 0:
                    st.session_state.vis_current -= 1
                    st.rerun()
        with nav_col3:
            st.markdown(f"""
            <div style="text-align:center; font-size:13px; color:#94a3b8; padding:8px 0;">
                Step {current + 1} / {total}
            </div>
            """, unsafe_allow_html=True)
        with nav_col4:
            if st.button("▶️", help="Next"):
                if current < total - 1:
                    st.session_state.vis_current += 1
                    st.rerun()
        with nav_col5:
            if st.button("⏭️", help="Last step"):
                st.session_state.vis_current = total - 1
                st.rerun()

        # Current step display
        col_left, col_right = st.columns([1, 1])

        with col_left:
            st.markdown(section_title_html("CURRENT LINE"), unsafe_allow_html=True)
            ln = step.get('line_number', '?')
            line_code = step.get('line', '')
            action = step.get('action', '')
            highlight = step.get('highlight', '')
            output = step.get('output', '')
            callstack = step.get('callstack', [])

            st.markdown(f"""
            <div class="glass-card">
                <div style="font-size:11px; color:#6366f1; font-weight:700; margin-bottom:8px;">
                    📍 LINE {ln}
                </div>
                <div class="line-highlight">
                    {line_code if line_code else '(entry point)'}
                </div>
                <div style="font-size:13px; color:#e2e8f0; margin:12px 0; line-height:1.6;">
                    <strong>What's happening:</strong><br/>{action}
                </div>
            """, unsafe_allow_html=True)

            if highlight:
                st.markdown(f"""
                <div class="info-box tip" style="margin-top:8px;">
                    <span>💡</span>
                    <span style="font-size:12px;">{highlight}</span>
                </div>
                """, unsafe_allow_html=True)

            if output:
                st.markdown(f"""
                <div style="background:rgba(16,185,129,0.08); border:1px solid rgba(16,185,129,0.2);
                    border-radius:8px; padding:10px 12px; margin-top:8px;">
                    <div style="font-size:11px; color:#10b981; font-weight:700; margin-bottom:4px;">
                        📤 OUTPUT
                    </div>
                    <code>{output}</code>
                </div>
                """, unsafe_allow_html=True)

            if callstack:
                st.markdown(f"""
                <div style="margin-top:10px;">
                    <div style="font-size:11px; color:#64748b; margin-bottom:6px;">📚 CALL STACK</div>
                    {"".join(f'<div style="font-size:12px; font-family:JetBrains Mono,monospace; color:#6366f1; padding:3px 8px; background:rgba(99,102,241,0.08); border-radius:4px; margin-bottom:3px;">→ {f}</div>' for f in reversed(callstack))}
                </div>
                """, unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

        with col_right:
            st.markdown(section_title_html("VARIABLE STATE"), unsafe_allow_html=True)
            variables = step.get("variables", {})
            changed_vars = step.get("changed_vars", [])

            if variables:
                st.markdown("""
                <div class="glass-card" style="overflow-x:auto;">
                    <table class="var-table" style="width:100%;">
                        <thead>
                            <tr>
                                <th>Variable</th>
                                <th>Value</th>
                                <th>Changed</th>
                            </tr>
                        </thead>
                        <tbody>
                """, unsafe_allow_html=True)

                for var, val in variables.items():
                    changed = var in changed_vars
                    change_icon = "⚡ NOW" if changed else ""
                    val_class = "var-changed" if changed else ""
                    row_bg = "background:rgba(34,211,238,0.04);" if changed else ""
                    st.markdown(f"""
                        <tr style="{row_bg}">
                            <td><code>{var}</code></td>
                            <td class="{val_class}"><code>{val}</code></td>
                            <td style="color:#22d3ee; font-size:11px; font-weight:600;">{change_icon}</td>
                        </tr>
                    """, unsafe_allow_html=True)

                st.markdown("</tbody></table></div>", unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="glass-card" style="text-align:center; color:#64748b; padding:30px 0;">
                    No variables yet at this step
                </div>
                """, unsafe_allow_html=True)

        # Key patterns
        if st.session_state.vis_patterns and current == total - 1:
            st.markdown(section_title_html("KEY PATTERNS IDENTIFIED"), unsafe_allow_html=True)
            badges_html = "".join(
                f'<span class="badge badge-blue">🔑 {p}</span>'
                for p in st.session_state.vis_patterns
            )
            st.markdown(f'<div style="margin:8px 0;">{badges_html}</div>', unsafe_allow_html=True)

    else:
        st.markdown("""
        <div style="text-align:center; padding:40px 0; color:#64748b;">
            <div style="font-size:48px; margin-bottom:12px;">🔬</div>
            <div style="font-size:15px; font-weight:600; color:#94a3b8; margin-bottom:6px;">
                Ready to visualize
            </div>
            <div style="font-size:13px;">Paste a small code snippet above and click Visualize!</div>
        </div>
        """, unsafe_allow_html=True)
