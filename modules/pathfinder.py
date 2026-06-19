import streamlit as st
from utils.groq_client import call_groq
from utils.styles import module_header_html, section_title_html, progress_bar_html

SYSTEM_PROMPT = """You are LogicPilot's Step-by-Step Pathfinder. Your job:
- User gives you a programming goal
- Generate a step-by-step logical path (5-8 steps) to achieve it
- Each step is a THINKING PROMPT, not a code answer
- Adapt difficulty based on skill level: Beginner, Intermediate, Advanced
- Each step ends with a question that makes the user THINK before moving forward
- Steps should build on each other like scaffolding

Format your response EXACTLY as JSON like this:
{
  "goal_summary": "brief restatement of the goal",
  "steps": [
    {
      "id": 1,
      "title": "Step title",
      "guidance": "What to think about here",
      "question": "One guiding question to ponder before moving on"
    }
  ]
}

Only return valid JSON. No extra text before or after."""

def render():
    st.markdown(module_header_html(
        "🗺️", "Step-by-Step Logic Pathfinder",
        "Tell me your goal — I'll guide you one step at a time, never giving away the full answer"
    ), unsafe_allow_html=True)

    st.markdown("""
    <div class="info-box philosophy">
        <span>🧭</span>
        <span>Like a GPS — "turn left here", not "here's your destination already."
        Each step only unlocks once you've attempted the previous one.</span>
    </div>
    """, unsafe_allow_html=True)

    # Init state
    if "path_steps" not in st.session_state:
        st.session_state.path_steps = []
    if "path_goal" not in st.session_state:
        st.session_state.path_goal = ""
    if "path_unlocked" not in st.session_state:
        st.session_state.path_unlocked = 1  # first step always unlocked
    if "path_completed" not in st.session_state:
        st.session_state.path_completed = set()

    # Goal input
    if not st.session_state.path_steps:
        st.markdown(section_title_html("YOUR GOAL"), unsafe_allow_html=True)

        goal = st.text_input(
            "Goal",
            placeholder="e.g. Build a user login system with password validation",
            label_visibility="collapsed",
            key="path_goal_input"
        )

        skill_level = st.radio(
            "Skill Level",
            ["🌱 Beginner", "🔥 Intermediate", "⚡ Advanced"],
            horizontal=True,
            key="path_skill"
        )

        if st.button("🗺️ Generate My Learning Path", use_container_width=False):
            if goal.strip():
                skill = skill_level.split(" ")[1]
                prompt = f"Goal: {goal}\nSkill level: {skill}\n\nGenerate a step-by-step learning path."
                with st.spinner("🗺️ Charting your path..."):
                    import json
                    raw = call_groq(SYSTEM_PROMPT, prompt)
                    try:
                        # Clean potential markdown code fences
                        cleaned = raw.strip()
                        if cleaned.startswith("```"):
                            cleaned = cleaned.split("```")[1]
                            if cleaned.startswith("json"):
                                cleaned = cleaned[4:]
                        data = json.loads(cleaned)
                        st.session_state.path_steps = data.get("steps", [])
                        st.session_state.path_goal = data.get("goal_summary", goal)
                        st.session_state.path_unlocked = 1
                        st.session_state.path_completed = set()
                        st.rerun()
                    except Exception as e:
                        st.error(f"Failed to parse path: {e}\n\nRaw: {raw[:300]}")
    else:
        # Show the path
        total = len(st.session_state.path_steps)
        done = len(st.session_state.path_completed)
        pct = int((done / total) * 100) if total else 0

        st.markdown(f"""
        <div class="glass-card">
            <div style="font-size:12px; color: #94a3b8; margin-bottom:6px;">
                🎯 <strong>Goal:</strong> {st.session_state.path_goal}
            </div>
            <div style="font-size:12px; color: #64748b; margin-bottom:8px;">
                {done} of {total} steps completed
            </div>
            {progress_bar_html(pct)}
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns([1, 5])
        with col1:
            if st.button("🔄 New Goal"):
                st.session_state.path_steps = []
                st.session_state.path_goal = ""
                st.session_state.path_unlocked = 1
                st.session_state.path_completed = set()
                st.rerun()

        st.markdown(section_title_html("YOUR LEARNING PATH"), unsafe_allow_html=True)

        for step in st.session_state.path_steps:
            sid = step.get("id", 0)
            is_locked = sid > st.session_state.path_unlocked
            is_done = sid in st.session_state.path_completed

            if is_done:
                status_icon = "✅"
                card_style = 'border:1px solid rgba(16,185,129,0.4); background:rgba(16,185,129,0.04); border-radius:12px; margin-bottom:10px; overflow:hidden;'
                num_class = "done-num"
            elif is_locked:
                status_icon = "🔒"
                card_style = 'border:1px solid rgba(99,102,241,0.1); background:rgba(17,24,39,0.4); border-radius:12px; margin-bottom:10px; opacity:0.45; overflow:hidden;'
                num_class = "locked-num"
            else:
                status_icon = "▶️"
                card_style = 'border:1px solid rgba(99,102,241,0.3); background:rgba(99,102,241,0.06); border-radius:12px; margin-bottom:10px; overflow:hidden; box-shadow:0 0 12px rgba(99,102,241,0.1);'
                num_class = ""

            with st.expander(
                f"{status_icon} Step {sid}: {step.get('title', '')}",
                expanded=(not is_locked and not is_done)
            ):
                if not is_locked:
                    st.markdown(f"""
                    <div style="font-size:14px; color:#e2e8f0; line-height:1.7; margin-bottom:12px;">
                        {step.get('guidance', '')}
                    </div>
                    <div class="debug-question">
                        <div class="q-label">🤔 Think About This</div>
                        {step.get('question', '')}
                    </div>
                    """, unsafe_allow_html=True)

                    if not is_done:
                        col_a, col_b = st.columns([2, 1])
                        with col_a:
                            attempt = st.text_area(
                                "Your attempt / answer",
                                placeholder="Write your thoughts or attempt here before unlocking the next step...",
                                height=90,
                                key=f"attempt_{sid}",
                                label_visibility="visible"
                            )
                        with col_b:
                            st.write("")  # spacer
                            st.write("")
                            if st.button(f"✅ Mark as Attempted", key=f"unlock_{sid}"):
                                st.session_state.path_completed.add(sid)
                                if sid + 1 <= total:
                                    st.session_state.path_unlocked = sid + 1
                                st.rerun()
                    else:
                        st.markdown('<span class="badge badge-green">✅ Completed</span>', unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div style="color:#64748b; font-size:13px; text-align:center; padding:12px;">
                        🔒 Complete the previous step to unlock this one
                    </div>
                    """, unsafe_allow_html=True)

        if done == total:
            st.markdown("""
            <div style="text-align:center; padding:24px; background: rgba(16,185,129,0.1);
                border-radius:12px; border:1px solid rgba(16,185,129,0.3); margin-top:16px;">
                <div style="font-size:32px; margin-bottom:8px;">🎉</div>
                <div style="font-size:18px; font-weight:700; color:#10b981;">Path Complete!</div>
                <div style="font-size:13px; color:#94a3b8; margin-top:6px;">
                    You worked through every step logically. Ready to implement?
                </div>
            </div>
            """, unsafe_allow_html=True)
