import streamlit as st
from utils.groq_client import call_groq
from utils.styles import module_header_html, section_title_html, complexity_meter_html

SYSTEM_PROMPT = """You are LogicPilot's Complexity Optimizer. Your job:
- Analyze user's code for time/space complexity
- Show 1-2 optimized alternatives
- NEVER say "yours is wrong" — say "yours works, here's what changes at scale"
- Be encouraging and educational

Format your response as EXACTLY this JSON structure:
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
    "approach_name": "Name of the optimized technique",
    "description": "What the optimized approach does",
    "time_complexity": "O(...)",
    "space_complexity": "O(...)",
    "complexity_score": 20,
    "readability": "High/Medium/Low",
    "works_well_for": "large inputs",
    "key_insight": "The key insight that makes this faster",
    "when_to_use": "When this optimization matters"
  },
  "scale_comparison": [
    {"input_size": "100 items", "user_time": "~0.01ms", "optimized_time": "~0.001ms"},
    {"input_size": "10,000 items", "user_time": "~100ms", "optimized_time": "~1ms"},
    {"input_size": "1,000,000 items", "user_time": "~Hours", "optimized_time": "~100ms"}
  ],
  "encouragement": "A short, genuine encouraging sentence"
}

Return ONLY the JSON, no extra text."""

COMPLEXITY_TO_PERCENT = {
    "O(1)": 5, "O(log n)": 10, "O(n)": 20, "O(n log n)": 35,
    "O(n²)": 70, "O(n³)": 90, "O(2^n)": 98, "O(n!)": 100
}

def complexity_to_bar(tc: str) -> int:
    for key, val in COMPLEXITY_TO_PERCENT.items():
        if key in tc:
            return val
    return 50

def render():
    st.markdown(module_header_html(
        "⚡", "Optimized Alternative Explainer",
        "Paste your working code — I'll show you what changes at scale, without saying yours is wrong"
    ), unsafe_allow_html=True)

    st.markdown("""
    <div class="info-box philosophy">
        <span>⚡</span>
        <span>Your code works. But what happens when it runs on 1 million items?
        This module shows you <em>why</em> some approaches shine at scale.</span>
    </div>
    """, unsafe_allow_html=True)

    if "opt_result" not in st.session_state:
        st.session_state.opt_result = None

    # ── Auto-sync from editor ─────────────────────────────────────────────────
    synced_code = st.session_state.pop("opt_synced_code", None)
    if synced_code:
        st.session_state["_opt_prefill"] = synced_code
        st.session_state.opt_result = None  # reset previous result

    prefill_code = st.session_state.get("_opt_prefill", "")

    if prefill_code:
        st.markdown("""
        <div class="info-box tip" style="margin-bottom:12px;">
            <span>📎</span>
            <span><strong>Editor code synced!</strong> Your code is pre-loaded and ready to optimize.</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(section_title_html("YOUR CODE"), unsafe_allow_html=True)

    code_input = st.text_area(
        "Paste your code",
        value=prefill_code if prefill_code else "",
        placeholder="# Paste your working code here...\n\ndef find_duplicates(arr):\n    duplicates = []\n    for i in range(len(arr)):\n        for j in range(i+1, len(arr)):\n            if arr[i] == arr[j] and arr[i] not in duplicates:\n                duplicates.append(arr[i])\n    return duplicates",
        height=200,
        label_visibility="collapsed",
        key="opt_code"
    )
    if prefill_code:
        st.markdown("""
        <div style="font-size:11px; color:#6366f1; margin-top:-8px; margin-bottom:4px;">
            📎 Auto-filled from editor
        </div>
        """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 4])
    with col1:
        analyze = st.button("⚡ Optimize!", use_container_width=True)
    with col2:
        if st.button("🗑️ Clear", use_container_width=False):
            st.session_state.opt_result = None
            st.rerun()

    if analyze and code_input.strip():
        with st.spinner("⚡ Analyzing complexity..."):
            import json
            raw = call_groq(SYSTEM_PROMPT, f"Analyze this code:\n\n```\n{code_input}\n```")
            try:
                cleaned = raw.strip()
                if cleaned.startswith("```"):
                    cleaned = cleaned.split("```")[1]
                    if cleaned.startswith("json"):
                        cleaned = cleaned[4:]
                st.session_state.opt_result = json.loads(cleaned)
                st.rerun()
            except Exception as e:
                st.error(f"Parse error: {e}")
                st.code(raw, language="text")

    if st.session_state.opt_result:
        d = st.session_state.opt_result
        ua = d.get("user_approach", {})
        op = d.get("optimized", {})
        scale = d.get("scale_comparison", [])

        # Encouragement banner
        st.markdown(f"""
        <div class="info-box tip">
            <span>✅</span>
            <span><strong>Your code works!</strong> {d.get('encouragement', '')}</span>
        </div>
        """, unsafe_allow_html=True)

        # Side-by-side comparison
        st.markdown(section_title_html("COMPARISON"), unsafe_allow_html=True)
        col_yours, col_opt = st.columns(2)

        with col_yours:
            st.markdown(f"""
            <div class="glass-card">
                <h3 style="color:#f59e0b;">📝 YOUR APPROACH</h3>
                <div style="font-size:13px; color:#94a3b8; margin-bottom:14px; line-height:1.6;">
                    {ua.get('description', '')}
                </div>
            """, unsafe_allow_html=True)

            tc = ua.get('time_complexity', 'O(?)')
            sc = ua.get('space_complexity', 'O(?)')
            bar = complexity_to_bar(tc)
            st.markdown(complexity_meter_html("⏱ Time", tc, bar, danger=bar > 40), unsafe_allow_html=True)
            st.markdown(f"""
                <div style="margin:10px 0; font-size:13px;">
                    <div style="color:#64748b; margin-bottom:6px;">Details</div>
                    <div class="complexity-row"><span class="complexity-label">Space</span>
                        <span class="complexity-value">{sc}</span></div>
                    <div class="complexity-row"><span class="complexity-label">Readability</span>
                        <span class="complexity-value">{ua.get('readability', '-')}</span></div>
                    <div class="complexity-row"><span class="complexity-label">Good for</span>
                        <span class="complexity-value">{ua.get('works_well_for', '-')}</span></div>
                    <div class="complexity-row"><span class="complexity-label">Strength</span>
                        <span class="complexity-value" style="color:#10b981;">✅</span></div>
                </div>
                <div style="font-size:12px; color:#94a3b8; margin-top:8px;">{ua.get('strength', '')}</div>
            </div>
            """, unsafe_allow_html=True)

        with col_opt:
            st.markdown(f"""
            <div class="glass-card" style="border-color:rgba(99,102,241,0.4);">
                <h3 style="color:#6366f1;">🚀 OPTIMIZED: {op.get('approach_name', 'Better Approach')}</h3>
                <div style="font-size:13px; color:#94a3b8; margin-bottom:14px; line-height:1.6;">
                    {op.get('description', '')}
                </div>
            """, unsafe_allow_html=True)

            tc2 = op.get('time_complexity', 'O(?)')
            sc2 = op.get('space_complexity', 'O(?)')
            bar2 = complexity_to_bar(tc2)
            st.markdown(complexity_meter_html("⏱ Time", tc2, bar2, danger=False), unsafe_allow_html=True)
            st.markdown(f"""
                <div style="margin:10px 0; font-size:13px;">
                    <div style="color:#64748b; margin-bottom:6px;">Details</div>
                    <div class="complexity-row"><span class="complexity-label">Space</span>
                        <span class="complexity-value">{sc2}</span></div>
                    <div class="complexity-row"><span class="complexity-label">Readability</span>
                        <span class="complexity-value">{op.get('readability', '-')}</span></div>
                    <div class="complexity-row"><span class="complexity-label">Good for</span>
                        <span class="complexity-value">{op.get('works_well_for', '-')}</span></div>
                    <div class="complexity-row"><span class="complexity-label">Key Insight</span>
                        <span class="complexity-value" style="color:#22d3ee;">💡</span></div>
                </div>
                <div style="font-size:12px; color:#22d3ee; margin-top:8px;">{op.get('key_insight', '')}</div>
            </div>
            """, unsafe_allow_html=True)

        # Scale comparison
        if scale:
            st.markdown(section_title_html("PERFORMANCE AT SCALE"), unsafe_allow_html=True)
            st.markdown("""
            <div class="glass-card">
                <table class="var-table" style="width:100%;">
                    <thead>
                        <tr>
                            <th>Input Size</th>
                            <th style="color:#f59e0b;">📝 Your Approach</th>
                            <th style="color:#6366f1;">🚀 Optimized</th>
                        </tr>
                    </thead>
                    <tbody>
            """, unsafe_allow_html=True)

            for row in scale:
                st.markdown(f"""
                        <tr>
                            <td><strong>{row.get('input_size', '')}</strong></td>
                            <td style="color:#f59e0b;">{row.get('user_time', '')}</td>
                            <td style="color:#10b981;">{row.get('optimized_time', '')}</td>
                        </tr>
                """, unsafe_allow_html=True)

            st.markdown("""
                    </tbody>
                </table>
            </div>
            """, unsafe_allow_html=True)

        # When to use
        if op.get("when_to_use"):
            st.markdown(f"""
            <div class="info-box warning">
                <span>💡</span>
                <span><strong>When to optimize:</strong> {op.get('when_to_use', '')}</span>
            </div>
            """, unsafe_allow_html=True)

    else:
        if not code_input:
            st.markdown("""
            <div style="text-align:center; padding:40px 0; color:#64748b;">
                <div style="font-size:48px; margin-bottom:12px;">⚡</div>
                <div style="font-size:15px; font-weight:600; color:#94a3b8; margin-bottom:6px;">
                    No code analyzed yet
                </div>
                <div style="font-size:13px;">Paste your working code above and click Optimize!</div>
            </div>
            """, unsafe_allow_html=True)
