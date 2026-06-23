"""
Visualizer module — step-by-step code execution visualizer.
Layout: Left small panel (current line) | Right large panel (full visualization).
"""
import streamlit as st
from utils.groq_client import call_groq
from utils.styles import module_header_html, section_title_html, panel_header_html

SYSTEM_PROMPT = """You are LogicAI's Visual Code Explainer. Simulate code execution step-by-step.

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
Be thorough — include EVERY significant operation. Show actual values.
Return ONLY valid JSON."""


def render():
    st.markdown(
        module_header_html(
            "🔬", "Visual Code Stepper",
            "Watch every variable change in slow motion — step by step"
        ),
        unsafe_allow_html=True,
    )

    # ── State init ────────────────────────────────────────────────────────────
    for key, default in [
        ("vis_steps",    []),
        ("vis_current",  0),
        ("vis_summary",  ""),
        ("vis_patterns", []),
    ]:
        if key not in st.session_state:
            st.session_state[key] = default

    # ── Auto-sync from editor ─────────────────────────────────────────────────
    synced = st.session_state.pop("vis_synced_code", None)
    if synced:
        st.session_state["_vis_prefill"] = synced
        st.session_state.vis_steps   = []
        st.session_state.vis_current = 0

    prefill = st.session_state.get("_vis_prefill", "")
    current_code = (
        st.session_state.get("editor_code", "")
        or prefill
        or ""
    )

    # ── Controls row ──────────────────────────────────────────────────────────
    ctrl_c1, ctrl_c2, ctrl_c3, ctrl_spacer = st.columns([2, 1.5, 1.5, 5])
    with ctrl_c1:
        if st.button("🔬 Visualize Code", use_container_width=True, key="vis_run_btn"):
            if current_code.strip():
                with st.spinner("🔬 Simulating execution…"):
                    import json
                    raw = call_groq(
                        SYSTEM_PROMPT,
                        f"Visualize this code step by step:\n\n```\n{current_code}\n```",
                    )
                    try:
                        cleaned = raw.strip()
                        if cleaned.startswith("```"):
                            cleaned = cleaned.split("```")[1]
                            if cleaned.startswith("json"):
                                cleaned = cleaned[4:]
                        data = json.loads(cleaned)
                        st.session_state.vis_steps    = data.get("steps", [])
                        st.session_state.vis_current  = 0
                        st.session_state.vis_summary  = data.get("summary", "")
                        st.session_state.vis_patterns = data.get("key_patterns", [])
                        st.rerun()
                    except Exception as e:
                        st.error(f"Parse error: {e}\n\nRaw: {raw[:300]}")
            else:
                st.warning("Write or load code in the editor first.")
    with ctrl_c2:
        if st.button("🗑️ Clear", key="vis_clear_btn", use_container_width=True):
            st.session_state.vis_steps   = []
            st.session_state.vis_current = 0
            st.rerun()
    with ctrl_c3:
        if prefill or current_code:
            st.markdown(
                f'<div class="lang-pill">📎 {st.session_state.get("editor_language","py").upper()}</div>',
                unsafe_allow_html=True,
            )

    if not st.session_state.vis_steps:
        # ── EMPTY STATE ───────────────────────────────────────────────────────
        col_cur, col_vis = st.columns([1, 3])

        with col_cur:
            st.markdown(
                panel_header_html("📍", "Current Line"),
                unsafe_allow_html=True,
            )
            # Show code from editor (small read-only mirror)
            if current_code.strip():
                lines = current_code.split("\n")
                lines_html = "".join(
                    f'<div class="line-inactive"><span style="color:#2d3748;margin-right:10px;">'
                    f'{i+1:2d}</span>{ln.replace("<","&lt;").replace(">","&gt;")}</div>'
                    for i, ln in enumerate(lines[:30])
                )
                st.markdown(
                    f'<div class="code-mirror" style="max-height:400px;overflow-y:auto;">'
                    f'{lines_html}</div>',
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    """
<div style="text-align:center;padding:40px 10px;color:#475569;">
    <div style="font-size:32px;margin-bottom:8px;">📍</div>
    <div style="font-size:12px;">Current line<br>appears here</div>
</div>
""",
                    unsafe_allow_html=True,
                )

        with col_vis:
            st.markdown(
                panel_header_html("🔬", "Visualizer — Full Execution"),
                unsafe_allow_html=True,
            )
            st.markdown(
                """
<div class="info-box philosophy">
    <span>🎬</span>
    <span>Like a slow-motion replay of what the computer is doing.
    Watch variables change, loops iterate, and your logic unfold — one step at a time.</span>
</div>
""",
                unsafe_allow_html=True,
            )
            st.markdown(
                """
<div style="text-align:center;padding:60px 20px;color:#475569;">
    <div style="font-size:56px;margin-bottom:12px;
        filter:drop-shadow(0 0 20px rgba(139,92,246,0.4));">🔬</div>
    <div style="font-size:16px;font-weight:600;color:#94a3b8;margin-bottom:6px;">
        Ready to visualize
    </div>
    <div style="font-size:13px;">
        Write code in the editor, then click <strong>Visualize Code</strong>
    </div>
</div>
""",
                unsafe_allow_html=True,
            )
        return

    # ══════════════════════════════════════════════════════════════════════════
    # ACTIVE VISUALIZATION
    # ══════════════════════════════════════════════════════════════════════════
    steps   = st.session_state.vis_steps
    current = st.session_state.vis_current
    total   = len(steps)
    step    = steps[current]
    active_ln = step.get("line_number", 0)

    col_cur, col_vis = st.columns([1, 3])

    # ── LEFT: Current Line Panel ──────────────────────────────────────────────
    with col_cur:
        st.markdown(
            panel_header_html("📍", "Current Line"),
            unsafe_allow_html=True,
        )

        # Code lines with current line highlighted
        if current_code.strip():
            code_lines = current_code.split("\n")
            lines_html = ""
            for i, ln in enumerate(code_lines[:60]):
                safe_ln = ln.replace("<", "&lt;").replace(">", "&gt;")
                lnum = i + 1
                if lnum == active_ln:
                    lines_html += (
                        f'<div class="line-active">'
                        f'<span style="color:#8b5cf6;margin-right:8px;font-weight:700;">{lnum:2d} ▶</span>'
                        f'{safe_ln}</div>'
                    )
                else:
                    lines_html += (
                        f'<div class="line-inactive">'
                        f'<span style="color:#2d3748;margin-right:10px;">{lnum:2d}</span>'
                        f'{safe_ln}</div>'
                    )
            st.markdown(
                f'<div class="code-mirror" style="max-height:480px;overflow-y:auto;">'
                f'{lines_html}</div>',
                unsafe_allow_html=True,
            )

        # Step info pill
        st.markdown(
            f"""
<div style="margin-top:10px;padding:8px 12px;
    background:rgba(139,92,246,0.08);border:1px solid rgba(139,92,246,0.2);
    border-radius:8px;font-size:12px;">
    <div style="color:#8b5cf6;font-weight:700;font-size:10px;
        letter-spacing:1px;text-transform:uppercase;margin-bottom:4px;">STEP</div>
    <div style="color:#f1f5f9;font-size:20px;font-weight:800;">{current+1}
        <span style="font-size:12px;color:#64748b;font-weight:400;">/ {total}</span>
    </div>
    <div class="progress-track" style="margin-top:6px;">
        <div class="progress-fill" style="width:{int(((current+1)/total)*100)}%;"></div>
    </div>
</div>
""",
            unsafe_allow_html=True,
        )

    # ── RIGHT: Full Visualization ──────────────────────────────────────────────
    with col_vis:
        st.markdown(
            panel_header_html("🔬", f"Execution — {st.session_state.vis_summary}"),
            unsafe_allow_html=True,
        )

        # Navigation controls
        nav1, nav2, nav_info, nav3, nav4 = st.columns([1, 1, 3, 1, 1])
        with nav1:
            if st.button("⏮", key="vis_first", help="First step"):
                st.session_state.vis_current = 0
                st.rerun()
        with nav2:
            if st.button("◀", key="vis_prev", help="Previous"):
                if current > 0:
                    st.session_state.vis_current -= 1
                    st.rerun()
        with nav_info:
            pct = int(((current + 1) / total) * 100)
            st.markdown(
                f"""
<div style="text-align:center;padding:6px 0;">
    <div style="font-size:13px;color:#94a3b8;margin-bottom:4px;">
        Step <strong style="color:#8b5cf6">{current+1}</strong> of {total}
        &nbsp;·&nbsp; Line <strong style="color:#06b6d4">{active_ln}</strong>
    </div>
    <div class="progress-track"><div class="progress-fill" style="width:{pct}%;"></div></div>
</div>
""",
                unsafe_allow_html=True,
            )
        with nav3:
            if st.button("▶", key="vis_next", help="Next"):
                if current < total - 1:
                    st.session_state.vis_current += 1
                    st.rerun()
        with nav4:
            if st.button("⏭", key="vis_last", help="Last step"):
                st.session_state.vis_current = total - 1
                st.rerun()

        st.markdown('<div style="height:8px;"></div>', unsafe_allow_html=True)

        # Step detail + variable state
        detail_col, var_col = st.columns([1, 1])

        with detail_col:
            st.markdown(section_title_html("WHAT'S HAPPENING"), unsafe_allow_html=True)
            ln_code  = step.get("line", "(entry)")
            action   = step.get("action", "")
            highlight = step.get("highlight", "")
            output   = step.get("output", "")
            callstack = step.get("callstack", [])

            st.markdown(
                f"""
<div class="glass-card">
    <div style="font-size:10px;color:#8b5cf6;font-weight:700;letter-spacing:1px;margin-bottom:8px;">
        📍 LINE {active_ln}
    </div>
    <div style="background:#0d1117;border:1px solid rgba(139,92,246,0.2);border-left:3px solid #8b5cf6;
        border-radius:0 6px 6px 0;padding:8px 12px;font-family:'JetBrains Mono',monospace;
        font-size:13px;color:#e2e8f0;margin-bottom:12px;">
        {ln_code.replace('<','&lt;').replace('>','&gt;')}
    </div>
    <div style="font-size:13px;color:#e2e8f0;line-height:1.65;margin-bottom:10px;">
        <strong>What's happening:</strong><br>{action}
    </div>
""",
                unsafe_allow_html=True,
            )

            if highlight:
                st.markdown(
                    f"""
<div class="info-box tip" style="font-size:12px;">
    <span>💡</span><span>{highlight}</span>
</div>
""",
                    unsafe_allow_html=True,
                )

            if output:
                st.markdown(
                    f"""
<div style="background:rgba(16,185,129,0.08);border:1px solid rgba(16,185,129,0.2);
    border-radius:8px;padding:10px 12px;margin-top:8px;">
    <div style="font-size:10px;color:#10b981;font-weight:700;
        letter-spacing:1px;text-transform:uppercase;margin-bottom:4px;">📤 OUTPUT</div>
    <code style="color:#10b981;">{output.replace('<','&lt;').replace('>','&gt;')}</code>
</div>
""",
                    unsafe_allow_html=True,
                )

            if callstack:
                stack_html = "".join(
                    f'<div style="font-size:12px;font-family:JetBrains Mono,monospace;'
                    f'color:#8b5cf6;padding:3px 8px;background:rgba(139,92,246,0.08);'
                    f'border-radius:4px;margin-bottom:3px;">→ {f}</div>'
                    for f in reversed(callstack)
                )
                st.markdown(
                    f"""
<div style="margin-top:10px;">
    <div style="font-size:10px;color:#475569;margin-bottom:6px;
        letter-spacing:1px;text-transform:uppercase;font-weight:700;">📚 CALL STACK</div>
    {stack_html}
</div>
""",
                    unsafe_allow_html=True,
                )

            st.markdown("</div>", unsafe_allow_html=True)

        with var_col:
            st.markdown(section_title_html("VARIABLE STATE"), unsafe_allow_html=True)
            variables   = step.get("variables", {})
            changed_vars = step.get("changed_vars", [])

            if variables:
                rows_html = ""
                for var, val in variables.items():
                    changed = var in changed_vars
                    row_bg  = "background:rgba(6,182,212,0.06);" if changed else ""
                    val_col = "#06b6d4" if changed else "#e2e8f0"
                    changed_label = "⚡ NOW" if changed else ""
                    rows_html += f"""
<tr style="{row_bg}">
    <td><code style="color:#8b5cf6">{var}</code></td>
    <td><code style="color:{val_col}">{str(val).replace('<','&lt;').replace('>','&gt;')}</code></td>
    <td style="color:#06b6d4;font-size:10px;font-weight:700;">{changed_label}</td>
</tr>"""
                st.markdown(
                    f"""
<div class="glass-card" style="overflow-x:auto;padding:12px;">
    <table class="var-table" style="width:100%;">
        <thead>
            <tr>
                <th>Variable</th><th>Value</th><th>Changed</th>
            </tr>
        </thead>
        <tbody>{rows_html}</tbody>
    </table>
</div>
""",
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    """
<div class="glass-card" style="text-align:center;color:#475569;padding:30px;">
    No variables at this step yet
</div>
""",
                    unsafe_allow_html=True,
                )

        # Key patterns (last step)
        if st.session_state.vis_patterns and current == total - 1:
            st.markdown(section_title_html("KEY PATTERNS IDENTIFIED"), unsafe_allow_html=True)
            badges = "".join(
                f'<span class="badge badge-violet">🔑 {p}</span>'
                for p in st.session_state.vis_patterns
            )
            st.markdown(f'<div style="margin:8px 0;">{badges}</div>', unsafe_allow_html=True)

            # Final output
            final_out = step.get("output", "") or ""
            if final_out:
                st.markdown(
                    f"""
<div class="info-box tip">
    <span>🏁</span>
    <span><strong>Final Output:</strong> <code>{final_out}</code></span>
</div>
""",
                    unsafe_allow_html=True,
                )
