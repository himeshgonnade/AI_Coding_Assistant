import streamlit as st
from utils.groq_client import call_groq_stream
from utils.styles import (
    module_header_html, ai_response_html, user_message_html,
    badge_html, section_title_html, glass_card_html
)

SYSTEM_PROMPT = """You are LogicPilot, an elite AI coding mentor. Your philosophy is:
"Don't give a man a fish — teach him to fish."

Your role in the Logic Understanding Engine:
1. When a user explains their approach or shares partial code, REFLECT back what you understand about their intent
2. Identify 1-3 logical gaps, wrong assumptions, or approach mismatches — label each as:
   - ✅ CORRECT: Something they got right
   - ⚠️ ASSUMPTION: An assumption they're making that may not hold
   - ❌ GAP: A logical gap or missing consideration
3. NEVER rewrite their code or give them the solution
4. Ask 1 clarifying question at the end to deepen their thinking
5. Keep responses concise, mentor-like, and encouraging

Format your response with:
- A "UNDERSTANDING" section: What I think you're trying to do
- An "ANALYSIS" section: Labeled observations (✅ / ⚠️ / ❌)
- A "THINK ABOUT" section: One guiding question
"""

def render():
    st.markdown(module_header_html(
        "🧩", "Logic Understanding Engine",
        "Explain your approach — I'll reflect back your mental model and find the gaps"
    ), unsafe_allow_html=True)

    # Philosophy box
    st.markdown("""
    <div class="info-box philosophy">
        <span>💬</span>
        <span>Share your code or explain your approach in plain English. I won't write code for you —
        I'll help you understand what you're actually trying to do.</span>
    </div>
    """, unsafe_allow_html=True)

    # Initialize session state
    if "logic_history" not in st.session_state:
        st.session_state.logic_history = []

    # ── Auto-sync from editor ─────────────────────────────────────────────────
    synced_code = st.session_state.pop("logic_synced_code", None)
    if synced_code:
        st.session_state["_logic_prefill"] = synced_code

    prefill_code = st.session_state.get("_logic_prefill", "")

    # Show sync banner if code came from editor
    if prefill_code:
        st.markdown("""
        <div class="info-box tip" style="margin-bottom:12px;">
            <span>📎</span>
            <span><strong>Editor code synced!</strong> Your code from the editor is pre-loaded below.
            Switch to \'Share your code\' mode to analyze it.</span>
        </div>
        """, unsafe_allow_html=True)

    # Input area
    st.markdown(section_title_html("YOUR APPROACH"), unsafe_allow_html=True)

    default_mode = "💻 Share your code" if prefill_code else "📝 Explain in plain English"
    input_mode = st.radio(
        "Input mode",
        ["📝 Explain in plain English", "💻 Share your code"],
        index=1 if prefill_code else 0,
        horizontal=True,
        label_visibility="collapsed"
    )

    if "English" in input_mode:
        user_input = st.text_area(
            "Describe your approach",
            placeholder="e.g. I'm using a for loop inside another for loop to find duplicate values in a list...",
            height=120,
            key="logic_text_input",
            label_visibility="collapsed"
        )
    else:
        default_code = prefill_code if prefill_code else ""
        user_input = st.text_area(
            "Paste your code",
            value=default_code,
            placeholder="# Paste your partial or complete code here...",
            height=160,
            key="logic_code_input",
            label_visibility="collapsed"
        )
        if default_code:
            st.markdown("""
            <div style="font-size:11px; color:#6366f1; margin-top:-8px; margin-bottom:4px;">
                📎 Auto-filled from editor
            </div>
            """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 5])
    with col1:
        analyze = st.button("🔍 Analyze My Logic", use_container_width=True)
    with col2:
        if st.button("🗑️ Clear History", use_container_width=False):
            st.session_state.logic_history = []
            st.rerun()

    if analyze and user_input.strip():
        mode_label = "approach" if "English" in input_mode else "code"
        full_input = f"Here is my {mode_label}:\n\n{user_input}"

        st.session_state.logic_history.append({"role": "user", "content": user_input})

        with st.spinner("🧠 Mapping your mental model..."):
            response_placeholder = st.empty()
            full_response = ""
            for chunk in call_groq_stream(SYSTEM_PROMPT, full_input):
                full_response += chunk
            st.session_state.logic_history.append({"role": "assistant", "content": full_response})
        st.rerun()

    # Display conversation history
    if st.session_state.logic_history:
        st.markdown(section_title_html("ANALYSIS SESSION"), unsafe_allow_html=True)
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        for msg in st.session_state.logic_history:
            if msg["role"] == "user":
                st.markdown(user_message_html(msg["content"]), unsafe_allow_html=True)
            else:
                st.markdown(ai_response_html(msg["content"]), unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Follow-up input
        st.markdown(section_title_html("FOLLOW UP"), unsafe_allow_html=True)
        follow_up = st.text_input(
            "Follow up",
            placeholder="Ask a follow-up or clarify your approach...",
            label_visibility="collapsed",
            key="logic_followup"
        )
        if st.button("💬 Reply", key="logic_reply_btn"):
            if follow_up.strip():
                st.session_state.logic_history.append({"role": "user", "content": follow_up})
                history_context = "\n".join([
                    f"{'User' if m['role']=='user' else 'LogicPilot'}: {m['content']}"
                    for m in st.session_state.logic_history[-6:]
                ])
                full_resp = ""
                for chunk in call_groq_stream(SYSTEM_PROMPT, history_context):
                    full_resp += chunk
                st.session_state.logic_history.append({"role": "assistant", "content": full_resp})
                st.rerun()
    else:
        # Empty state
        st.markdown("""
        <div style="text-align:center; padding: 40px 0; color: #64748b;">
            <div style="font-size: 48px; margin-bottom: 12px;">🧩</div>
            <div style="font-size: 15px; font-weight: 600; margin-bottom: 6px; color: #94a3b8;">
                No analysis yet
            </div>
            <div style="font-size: 13px;">
                Describe your approach above and click Analyze
            </div>
        </div>
        """, unsafe_allow_html=True)
