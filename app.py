import streamlit as st
from streamlit_ace import st_ace
from utils.styles import inject_css, logo_html, section_title_html
import modules.logic_engine as logic_engine
import modules.pathfinder as pathfinder
import modules.optimizer as optimizer
import modules.visualizer as visualizer
import modules.debugger as debugger

# ─── PAGE CONFIG ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="LogicPilot — AI Coding Mentor",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── CSS ────────────────────────────────────────────────────────────────────────
inject_css()

# ─── SESSION STATE INIT ─────────────────────────────────────────────────────────
if "active_module" not in st.session_state:
    st.session_state.active_module = "editor"
if "editor_code" not in st.session_state:
    st.session_state.editor_code = '# Welcome to LogicPilot!\n# Write your code here and use the AI Mentor panels on the right.\n\ndef greet(name):\n    """A simple greeting function."""\n    return f"Hello, {name}!"\n\nprint(greet("World"))\n'
if "editor_language" not in st.session_state:
    st.session_state.editor_language = "python"

def sync_editor_to_modules():
    """Push current editor code into all module input states."""
    code = st.session_state.editor_code
    if code.strip():
        st.session_state["logic_synced_code"] = code
        st.session_state["opt_synced_code"] = code
        st.session_state["vis_synced_code"] = code
        st.session_state["debug_synced_code"] = code

# ─── SIDEBAR ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(logo_html(), unsafe_allow_html=True)

    # Editor code sync status
    has_code = bool(st.session_state.get("editor_code", "").strip())
    if has_code:
        lines = len(st.session_state.editor_code.strip().split('\n'))
        st.markdown(f"""
        <div style="background:rgba(99,102,241,0.08); border:1px solid rgba(99,102,241,0.2);
            border-radius:8px; padding:10px 12px; margin-bottom:14px;">
            <div style="font-size:10px; color:#6366f1; font-weight:700; letter-spacing:1px; margin-bottom:4px;">💻 EDITOR CODE</div>
            <div style="font-size:12px; color:#94a3b8;">🟢 {lines} lines ready — all modules synced</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Module Navigation
    st.markdown(section_title_html("WORKSPACE"), unsafe_allow_html=True)

    modules = [
        ("editor",       "💻", "Code Editor",              "Write & run any code"),
        ("logic",        "🧩", "Logic Understanding",       "Reflect your mental model"),
        ("pathfinder",   "🗺️", "Step-by-Step Pathfinder",  "Guided goal decomposition"),
        ("optimizer",    "⚡", "Complexity Optimizer",      "See how your code scales"),
        ("visualizer",   "🔬", "Visual Code Stepper",       "Watch execution in slow-mo"),
        ("debugger",     "🐛", "Debugging Partner",         "Find bugs Socratically"),
    ]

    for key, icon, label, desc in modules:
        is_active = st.session_state.active_module == key
        btn_style = f"""
        <div onclick="" style="
            display:flex; align-items:center; gap:10px;
            padding:11px 14px; border-radius:8px; margin-bottom:4px;
            cursor:pointer; transition:all 0.2s;
            background:{'linear-gradient(135deg,rgba(99,102,241,0.2),rgba(34,211,238,0.1))' if is_active else 'transparent'};
            border:1px solid {'rgba(99,102,241,0.5)' if is_active else 'transparent'};
        ">
            <span style="font-size:16px;">{icon}</span>
            <div>
                <div style="font-size:13px; font-weight:{'700' if is_active else '500'};
                    color:{'#6366f1' if is_active else '#94a3b8'};">{label}</div>
                <div style="font-size:10px; color:#4b5563;">{desc}</div>
            </div>
        </div>
        """
        if st.button(f"{icon} {label}", key=f"nav_{key}", use_container_width=True):
            st.session_state.active_module = key
            sync_editor_to_modules()
            st.rerun()

    st.markdown("---")

    # Language selector (shown for editor mode)
    if st.session_state.active_module == "editor":
        st.markdown(section_title_html("EDITOR SETTINGS"), unsafe_allow_html=True)
        languages = ["python", "javascript", "typescript", "java", "cpp", "c", "go", "rust",
                     "html", "css", "sql", "bash", "json", "markdown"]
        lang = st.selectbox(
            "Language",
            languages,
            index=languages.index(st.session_state.editor_language),
            key="lang_selector"
        )
        st.session_state.editor_language = lang

    # Sidebar footer
    st.markdown("""
    <div class="sidebar-footer">
        🧠 LogicPilot v1.0<br>
        <span style="color:#4b5563;">Powered by Groq + Llama 3.3</span>
    </div>
    """, unsafe_allow_html=True)

# ─── MAIN CONTENT ───────────────────────────────────────────────────────────────
if st.session_state.active_module == "editor":
    # ── EDITOR MODULE ──────────────────────────────────────────────────────────
    col_editor, col_ai = st.columns([3, 2])

    with col_editor:
        st.markdown("""
        <div style="display:flex; align-items:center; gap:10px; margin-bottom:12px;">
            <span style="font-size:18px;">💻</span>
            <div>
                <div style="font-size:18px; font-weight:700; background:linear-gradient(135deg,#6366f1,#22d3ee);
                    -webkit-background-clip:text; -webkit-text-fill-color:transparent;">
                    Code Editor
                </div>
                <div style="font-size:11px; color:#64748b;">Write any code — use the AI Mentor panel →</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        code = st_ace(
            value=st.session_state.editor_code,
            language=st.session_state.editor_language,
            theme="tomorrow_night_eighties",
            key="main_editor",
            height=520,
            font_size=14,
            tab_size=4,
            show_gutter=True,
            show_print_margin=False,
            wrap=False,
            auto_update=True,
            keybinding="vscode",
        )
        if code is not None:
            st.session_state.editor_code = code

        # Editor action bar
        st.markdown('<div style="margin-top:8px;"></div>', unsafe_allow_html=True)
        col_a, col_b, col_c, col_d = st.columns([1, 1, 1, 1])
        with col_a:
            if st.button("🧩 Logic", use_container_width=True, key="send_logic"):
                sync_editor_to_modules()
                st.session_state.active_module = "logic"
                st.rerun()
        with col_b:
            if st.button("⚡ Optimize", use_container_width=True, key="send_opt"):
                sync_editor_to_modules()
                st.session_state.active_module = "optimizer"
                st.rerun()
        with col_c:
            if st.button("🔬 Visualize", use_container_width=True, key="send_vis"):
                sync_editor_to_modules()
                st.session_state.active_module = "visualizer"
                st.rerun()
        with col_d:
            if st.button("🐛 Debug", use_container_width=True, key="send_debug"):
                sync_editor_to_modules()
                st.session_state.active_module = "debugger"
                st.rerun()

    with col_ai:
        st.markdown("""
        <div style="display:flex; align-items:center; gap:10px; margin-bottom:12px;">
            <span style="font-size:18px;">🧠</span>
            <div>
                <div style="font-size:18px; font-weight:700; background:linear-gradient(135deg,#6366f1,#22d3ee);
                    -webkit-background-clip:text; -webkit-text-fill-color:transparent;">
                    AI Mentor Panel
                </div>
                <div style="font-size:11px; color:#64748b;">Quick AI tools for your current code</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        tab1, tab2, tab3 = st.tabs(["🧩 Analyze Logic", "⚡ Optimize", "🐛 Debug Help"])

        with tab1:
            explain_query = st.text_area(
                "Explain your approach",
                placeholder="What are you trying to do with this code?",
                height=80,
                key="editor_logic_query",
                label_visibility="collapsed"
            )
            if st.button("🧩 Analyze", key="editor_analyze_btn", use_container_width=True):
                if explain_query.strip() or st.session_state.editor_code.strip():
                    from utils.groq_client import call_groq_stream
                    code_ctx = st.session_state.editor_code
                    query = explain_query or "Analyze what I'm trying to do."
                    system = """You are LogicPilot. Reflect the user's mental model, identify logical gaps (labeled ✅/⚠️/❌),
                    and ask one guiding question. NEVER write code for them. Keep it concise and mentor-like."""
                    prompt = f"My code:\n```\n{code_ctx}\n```\n\nMy approach/question: {query}"
                    with st.spinner("🧩 Analyzing..."):
                        response = ""
                        for chunk in call_groq_stream(system, prompt):
                            response += chunk
                    st.markdown(f"""
                    <div class="ai-response">
                        <div class="ai-label">🧩 Logic Analysis</div>
                        {response.replace(chr(10), '<br>')}
                    </div>
                    """, unsafe_allow_html=True)

        with tab2:
            if st.button("⚡ Quick Optimize", key="editor_opt_btn", use_container_width=True):
                if st.session_state.editor_code.strip():
                    from utils.groq_client import call_groq
                    system = """Give a quick complexity analysis of the code. Show time/space complexity,
                    one optimization idea, and why it matters at scale. Be concise (4-6 lines max). No code rewrites."""
                    with st.spinner("⚡ Analyzing complexity..."):
                        resp = call_groq(system, f"Code:\n```\n{st.session_state.editor_code}\n```")
                    st.markdown(f"""
                    <div class="ai-response">
                        <div class="ai-label">⚡ Quick Optimization Tips</div>
                        {resp.replace(chr(10), '<br>')}
                    </div>
                    """, unsafe_allow_html=True)

        with tab3:
            error_input = st.text_area(
                "Error or problem",
                placeholder="What error are you seeing? Or describe the unexpected behavior...",
                height=80,
                key="editor_error_input",
                label_visibility="collapsed"
            )
            if st.button("🐛 Get First Hint", key="editor_debug_btn", use_container_width=True):
                if error_input.strip():
                    from utils.groq_client import call_groq
                    system = """You are LogicPilot debugging helper. NEVER give the answer.
                    Ask ONE Socratic question to start them thinking. Suggest one print statement to add."""
                    prompt = f"Code:\n```\n{st.session_state.editor_code}\n```\nError: {error_input}"
                    with st.spinner("🔍 Thinking..."):
                        resp = call_groq(system, prompt)
                    st.markdown(f"""
                    <div class="debug-question">
                        <div class="q-label">🐛 First Debugging Clue</div>
                        {resp.replace(chr(10), '<br>')}
                    </div>
                    """, unsafe_allow_html=True)

        # Quick stats card
        if st.session_state.editor_code.strip():
            lines = st.session_state.editor_code.strip().split('\n')
            non_empty = [l for l in lines if l.strip() and not l.strip().startswith('#')]
            st.markdown(f"""
            <div class="glass-card" style="margin-top:16px;">
                <div style="font-size:11px; color:#64748b; font-weight:700; letter-spacing:1px; margin-bottom:10px;">
                    📊 CODE STATS
                </div>
                <div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:8px; text-align:center;">
                    <div>
                        <div style="font-size:22px; font-weight:700; color:#6366f1;">{len(lines)}</div>
                        <div style="font-size:10px; color:#64748b;">Lines</div>
                    </div>
                    <div>
                        <div style="font-size:22px; font-weight:700; color:#22d3ee;">{len(non_empty)}</div>
                        <div style="font-size:10px; color:#64748b;">Code Lines</div>
                    </div>
                    <div>
                        <div style="font-size:22px; font-weight:700; color:#10b981;">{len(st.session_state.editor_code)}</div>
                        <div style="font-size:10px; color:#64748b;">Characters</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

elif st.session_state.active_module == "logic":
    logic_engine.render()

elif st.session_state.active_module == "pathfinder":
    pathfinder.render()

elif st.session_state.active_module == "optimizer":
    optimizer.render()

elif st.session_state.active_module == "visualizer":
    visualizer.render()

elif st.session_state.active_module == "debugger":
    debugger.render()
