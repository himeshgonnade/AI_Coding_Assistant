"""
LogicAI — Code Intelligence Platform
Main application entry point.
"""
import streamlit as st
from streamlit_ace import st_ace
import streamlit.components.v1 as components

from utils.styles import inject_css, panel_header_html, section_title_html
from utils.code_runner import run_code
import modules.logic_engine as logic_engine
import modules.pathfinder as pathfinder
import modules.optimizer as optimizer
import modules.visualizer as visualizer
import modules.debugger as debugger

# ─── PAGE CONFIG ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="LogicAI — Code Intelligence Platform",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed",
)

inject_css()

# ─── SESSION STATE DEFAULTS ──────────────────────────────────────────────────
_DEFAULTS = {
    "active_page":      "compiler",
    "editor_code":      '# Welcome to LogicAI!\n# Write your code and use the AI Mentor panel on the right.\n\ndef greet(name):\n    return f"Hello, {name}!"\n\nprint(greet("World"))\n',
    "editor_language":  "python",
    "show_lang_menu":   False,
    "chat_history":     [],   # compiler-page chatbot
    "output_text":      "",
    "output_error":     "",
    "has_run":          False,
    "is_running":       False,
    "show_output":      False,
}
for _k, _v in _DEFAULTS.items():
    if _k not in st.session_state:
        st.session_state[_k] = _v

LANGUAGES = [
    "python", "javascript", "typescript", "java", "cpp", "c",
    "go", "rust", "html", "css", "sql", "bash", "json", "markdown",
]

LANG_ICONS = {
    "python": "🐍", "javascript": "🟨", "typescript": "🔷", "java": "☕",
    "cpp": "⚙️", "c": "⚙️", "go": "🐹", "rust": "🦀",
    "html": "🌐", "css": "🎨", "sql": "🗄️", "bash": "🐚",
    "json": "📋", "markdown": "📝",
}

ACE_THEMES = {
    "python": "tomorrow_night_eighties",
    "javascript": "dracula", "typescript": "dracula",
    "java": "tomorrow_night_blue", "cpp": "monokai",
    "c": "monokai", "go": "tomorrow_night",
    "rust": "tomorrow_night_eighties",
}


def get_ace_theme():
    return ACE_THEMES.get(st.session_state.editor_language, "tomorrow_night_eighties")


# ─── NAVIGATION HELPERS ──────────────────────────────────────────────────────
def sync_code_to_modules():
    code = st.session_state.editor_code
    for key in ("debug_synced_code", "opt_synced_code", "vis_synced_code", "logic_synced_code"):
        st.session_state[key] = code


def navigate_to(page: str):
    st.session_state.active_page = page
    st.session_state.show_lang_menu = False
    if page != "compiler":
        sync_code_to_modules()
    st.rerun()


# ─── JS: DRAG-RESIZABLE PANELS ───────────────────────────────────────────────
_RESIZE_JS = """
<script>
(function () {
    var WIN = window.parent;
    var DOC = WIN.document;
    var STORE_H = 'lai_left_pct';

    /* ── helpers ── */
    function clamp(v, lo, hi) { return Math.max(lo, Math.min(hi, v)); }
    function getBlocks() {
        /* The first stHorizontalBlock in main content area = nav.
           The second stHorizontalBlock = editor + right panel. */
        return DOC.querySelectorAll(
            '.main [data-testid="stHorizontalBlock"]'
        );
    }
    function getNavButtons() {
        var blocks = getBlocks();
        if (!blocks.length) return null;
        return blocks[0].querySelectorAll('[data-testid="stButton"] button');
    }

    /* ── apply active nav state ── */
    function applyNavActive() {
        var activeLabel = WIN.__LAI_ACTIVE || '';
        var btns = getNavButtons();
        if (!btns) return;
        btns.forEach(function(btn) {
            btn.style.removeProperty('background');
            btn.style.removeProperty('color');
            btn.style.removeProperty('border-color');
            btn.style.removeProperty('box-shadow');
        });
        var MAP = {
            compiler:   '▶',
            debugger:   'Debugger',
            visualizer: 'Visualizer',
            optimizer:  'Optimizer',
        };
        var needle = MAP[activeLabel] || '';
        if (!needle) return;
        btns.forEach(function(btn) {
            if (btn.textContent.indexOf(needle) !== -1) {
                btn.style.setProperty('background', 'linear-gradient(135deg,#8b5cf6,#06b6d4)', 'important');
                btn.style.setProperty('color', 'white', 'important');
                btn.style.setProperty('border-color', 'transparent', 'important');
                btn.style.setProperty('box-shadow', '0 4px 15px rgba(139,92,246,0.45)', 'important');
            }
        });
    }

    /* ── horizontal resize ── */
    function setupHResize() {
        var blocks = getBlocks();
        /* Second horizontal block contains the two main columns */
        var contentBlock = null;
        for (var i = 0; i < blocks.length; i++) {
            var cols = blocks[i].querySelectorAll(':scope > [data-testid="column"]');
            if (cols.length >= 2) { contentBlock = blocks[i]; break; }
        }
        if (!contentBlock) return;
        if (contentBlock.querySelector('.lai-h-handle')) return;

        var leftCol  = contentBlock.querySelectorAll(':scope > [data-testid="column"]')[0];
        var rightCol = contentBlock.querySelectorAll(':scope > [data-testid="column"]')[1];
        var savedPct = parseFloat(localStorage.getItem(STORE_H) || '50');

        function applyH(pct) {
            pct = clamp(pct, 22, 78);
            leftCol.style.setProperty('flex',      '0 0 ' + pct + '%', 'important');
            leftCol.style.setProperty('max-width', pct + '%',           'important');
            rightCol.style.setProperty('flex',      '0 0 ' + (100-pct) + '%', 'important');
            rightCol.style.setProperty('max-width', (100-pct) + '%',          'important');
        }
        applyH(savedPct);

        var handle = DOC.createElement('div');
        handle.className = 'lai-h-handle';
        handle.style.cssText = [
            'width:12px', 'cursor:col-resize', 'flex-shrink:0',
            'display:flex', 'align-items:center', 'justify-content:center',
            'border-radius:6px', 'background:transparent', 'transition:background 0.2s',
            'z-index:100', 'position:relative'
        ].join(';');

        var pill = DOC.createElement('div');
        pill.style.cssText = [
            'width:4px', 'height:56px', 'border-radius:2px',
            'background:linear-gradient(180deg,rgba(139,92,246,.45),rgba(6,182,212,.35))',
            'pointer-events:none', 'transition:all 0.2s'
        ].join(';');
        handle.appendChild(pill);

        handle.addEventListener('mouseenter', function() {
            pill.style.background = 'linear-gradient(180deg,#8b5cf6,#06b6d4)';
            pill.style.height = '72px';
            handle.style.background = 'rgba(139,92,246,0.08)';
        });
        handle.addEventListener('mouseleave', function() {
            if (!isH) {
                pill.style.background = 'linear-gradient(180deg,rgba(139,92,246,.45),rgba(6,182,212,.35))';
                pill.style.height = '56px';
                handle.style.background = 'transparent';
            }
        });

        contentBlock.insertBefore(handle, rightCol);

        var isH = false, hStartX, hStartW;
        handle.addEventListener('mousedown', function(e) {
            isH = true;
            hStartX = e.clientX;
            hStartW = leftCol.getBoundingClientRect().width;
            DOC.body.style.cursor = 'col-resize';
            DOC.body.style.userSelect = 'none';
            e.preventDefault();
        });
        DOC.addEventListener('mousemove', function(e) {
            if (!isH) return;
            var total = contentBlock.getBoundingClientRect().width;
            if (!total) return;
            var newW = hStartW + (e.clientX - hStartX);
            var pct  = (newW / total) * 100;
            applyH(pct);
            localStorage.setItem(STORE_H, pct.toFixed(1));
        });
        DOC.addEventListener('mouseup', function() {
            if (!isH) return;
            isH = false;
            DOC.body.style.cursor = '';
            DOC.body.style.userSelect = '';
            pill.style.background = 'linear-gradient(180deg,rgba(139,92,246,.45),rgba(6,182,212,.35))';
            pill.style.height = '56px';
            handle.style.background = 'transparent';
        });
    }

    /* ── vertical resize removed as per layout update ── */
    function setupVResize() {
        // Output and Chat panels are now toggled, not split vertically.
    }

    /* ── MutationObserver re-init ── */
    function run() {
        applyNavActive();
        setupHResize();
        setupVResize();
    }

    var observer = new MutationObserver(function() {
        setTimeout(run, 250);
    });

    function start() {
        var app = DOC.querySelector('[data-testid="stAppViewContainer"]');
        if (app) {
            observer.observe(app, { childList: true, subtree: true });
            run();
        } else {
            setTimeout(start, 300);
        }
    }

    start();
})();
</script>
"""


# ─── TOP NAVIGATION ──────────────────────────────────────────────────────────
def render_top_nav():
    active = st.session_state.active_page
    lang   = st.session_state.editor_language
    lang_icon = LANG_ICONS.get(lang, "💻")

    # Logo row (rendered via markdown)
    st.markdown(
        f"""
<div style="
    display:flex; align-items:center; gap:12px;
    padding:10px 24px 6px;
    background:linear-gradient(180deg,#0d1428,#080f1e);
    border-bottom:1px solid rgba(139,92,246,0.12);
">
    <div style="
        width:38px; height:38px; border-radius:10px; flex-shrink:0;
        background:linear-gradient(135deg,#8b5cf6,#06b6d4);
        display:flex; align-items:center; justify-content:center;
        font-size:20px; box-shadow:0 0 20px rgba(139,92,246,0.4);
    ">🧠</div>
    <div>
        <div style="
            font-size:18px; font-weight:800; letter-spacing:-0.5px;
            background:linear-gradient(135deg,#8b5cf6,#06b6d4);
            -webkit-background-clip:text; -webkit-text-fill-color:transparent;
            background-clip:text;
        ">LogicAI</div>
        <div style="font-size:9px;font-weight:700;letter-spacing:2px;color:#475569;text-transform:uppercase;">
            Code Intelligence Platform
        </div>
    </div>
    <div style="flex:1"></div>
    <div class="lang-pill">{lang_icon} {lang.upper()}</div>
</div>
""",
        unsafe_allow_html=True,
    )

    # Nav button row
    nav_col1, nav_col2, nav_col3, nav_col4, nav_col5, nav_spacer = st.columns(
        [1.4, 1.8, 1.4, 1.4, 1.4, 4]
    )
    with nav_col1:
        if st.button("🌐 Language", key="nav_lang", use_container_width=True):
            st.session_state.show_lang_menu = not st.session_state.show_lang_menu
            st.rerun()
    with nav_col2:
        if st.button("▶ Compile & Run", key="nav_compiler", use_container_width=True):
            navigate_to("compiler")
    with nav_col3:
        if st.button("🐛 Debugger", key="nav_debugger", use_container_width=True):
            navigate_to("debugger")
    with nav_col4:
        if st.button("🔬 Visualizer", key="nav_visualizer", use_container_width=True):
            navigate_to("visualizer")
    with nav_col5:
        if st.button("⚡ Optimizer", key="nav_optimizer", use_container_width=True):
            navigate_to("optimizer")

    # Horizontal rule after nav
    st.markdown(
        '<div style="height:1px;background:rgba(139,92,246,0.12);margin:0 0 4px;"></div>',
        unsafe_allow_html=True,
    )

    # Language selector dropdown
    if st.session_state.show_lang_menu:
        with st.container():
            st.markdown(section_title_html("SELECT LANGUAGE"), unsafe_allow_html=True)
            _cols = st.columns(7)
            for i, _lang in enumerate(LANGUAGES):
                with _cols[i % 7]:
                    _icon = LANG_ICONS.get(_lang, "💻")
                    if st.button(
                        f"{_icon} {_lang.upper()}",
                        key=f"lang_{_lang}",
                        use_container_width=True,
                        type="primary" if _lang == st.session_state.editor_language else "secondary",
                    ):
                        st.session_state.editor_language = _lang
                        st.session_state.show_lang_menu = False
                        st.rerun()
            st.markdown(
                '<div style="height:1px;background:rgba(139,92,246,0.12);margin:8px 0;"></div>',
                unsafe_allow_html=True,
            )


# ─── COMPILER PAGE ────────────────────────────────────────────────────────────
def render_compiler_page():
    col_editor, col_right = st.columns([1, 1])

    # ── LEFT: Code Editor ──────────────────────────────────────────────────────
    with col_editor:
        h_col1, h_col2 = st.columns([3, 1])
        with h_col1:
            st.markdown(
                panel_header_html("💻", "Code Editor"),
                unsafe_allow_html=True,
            )
        with h_col2:
            st.markdown('<div style="height: 4px;"></div>', unsafe_allow_html=True)
            if st.button("▶ Run Code", key="run_code_btn_top", use_container_width=True, type="primary"):
                st.session_state.is_running = True
                st.session_state.show_output = True
                with st.spinner("⚙️  Executing…"):
                    stdout, stderr = run_code(
                        st.session_state.editor_code,
                        st.session_state.editor_language,
                    )
                st.session_state.output_text  = stdout
                st.session_state.output_error = stderr
                st.session_state.has_run      = True
                st.session_state.is_running   = False
                st.rerun()

        code = st_ace(
            value=st.session_state.editor_code,
            language=st.session_state.editor_language,
            theme=get_ace_theme(),
            key="main_editor",
            height=560,
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

        # Code stats bar
        if st.session_state.editor_code.strip():
            lines_     = st.session_state.editor_code.strip().split("\n")
            code_lines = [l for l in lines_ if l.strip() and not l.strip().startswith("#")]
            st.markdown(
                f"""
<div style="
    display:flex; gap:20px; padding:10px 14px; margin-top:6px;
    background:rgba(139,92,246,0.05); border:1px solid rgba(139,92,246,0.12);
    border-radius:10px; font-size:12px; color:#64748b;
">
    <span>📄 <strong style='color:#94a3b8'>{len(lines_)}</strong> lines</span>
    <span>💻 <strong style='color:#94a3b8'>{len(code_lines)}</strong> code lines</span>
    <span>📝 <strong style='color:#94a3b8'>{len(st.session_state.editor_code)}</strong> chars</span>
    <span>🌐 <strong style='color:#06b6d4'>{st.session_state.editor_language.upper()}</strong></span>
</div>
""",
                unsafe_allow_html=True,
            )

    # ── RIGHT: Chatbot OR Output ────────────────────────────────────────────────
    with col_right:
        if st.session_state.show_output:
            # ─ Output panel ───────────────────────────────────────────────
            st.markdown(
                '<div id="lai-output-panel" style="display:flex;flex-direction:column;min-height:160px;">',
                unsafe_allow_html=True,
            )
            
            o_col1, o_col2 = st.columns([5, 1])
            with o_col1:
                st.markdown(
                    panel_header_html("📤", "Output"),
                    unsafe_allow_html=True,
                )
            with o_col2:
                st.markdown('<div style="height: 4px;"></div>', unsafe_allow_html=True)
                if st.button("❌", key="close_out_btn", use_container_width=True):
                    st.session_state.show_output = False
                    st.rerun()

            if st.session_state.has_run:
                if st.session_state.output_text:
                    st.markdown(
                        f"""
<div style="
    background:#0d1117; border:1px solid rgba(16,185,129,0.25);
    border-radius:10px; padding:12px 14px; margin-top:8px;
    font-family:'JetBrains Mono',monospace; font-size:12.5px;
    color:#10b981; white-space:pre-wrap; overflow-x:auto;
    max-height:500px; overflow-y:auto;
">{st.session_state.output_text.replace('<','&lt;').replace('>','&gt;')}</div>
""",
                        unsafe_allow_html=True,
                    )
                if st.session_state.output_error:
                    st.markdown(
                        f'<div class="lai-output-error">{st.session_state.output_error.replace("<","&lt;").replace(">","&gt;")}</div>',
                        unsafe_allow_html=True,
                    )
            else:
                st.markdown(
                    """
<div class="lai-output-empty">
    <span>▶</span> Click <strong>Run Code</strong> to see output
</div>
""",
                    unsafe_allow_html=True,
                )

            st.markdown("</div>", unsafe_allow_html=True)  # close lai-output-panel
            
        else:
            # ─ Chatbot panel ─────────────────────────────────────────────
            st.markdown(
                '<div id="lai-chat-panel" style="display:flex;flex-direction:column;">',
                unsafe_allow_html=True,
            )
            st.markdown(
                panel_header_html("🧠", "AI Logic Mentor"),
                unsafe_allow_html=True,
            )
            st.markdown(
                """
<div style="padding:8px 14px 4px;font-size:11px;color:#475569;
    border-bottom:1px solid rgba(139,92,246,0.08);">
    ✨ I guide your <em>thinking</em> — I won't write the code for you.
</div>
""",
                unsafe_allow_html=True,
            )

            # Chat history display
            chat_html = ""
            for msg in st.session_state.chat_history[-12:]:
                if msg["role"] == "user":
                    safe = msg["content"].replace("<", "&lt;").replace(">", "&gt;")
                    chat_html += f'<div class="chat-bubble-user">{safe}</div>'
                else:
                    safe = msg["content"].replace("<", "&lt;").replace(">", "&gt;")
                    chat_html += f"""
<div class="chat-bubble-ai">
    <div class="ai-label">🧠 LogicAI Mentor</div>
    {safe}
</div>"""

            if not chat_html:
                chat_html = """
<div style='color:#475569;font-size:12px;text-align:center;padding:24px 0;'>
    <div style='font-size:28px;margin-bottom:8px;'>🧠</div>
    Ask me about your code logic,<br>algorithms, or approach!
</div>"""

            st.markdown(
                f'<div class="chat-scroll" style="max-height:500px;">{chat_html}</div>',
                unsafe_allow_html=True,
            )

            # Chat input
            with st.form("compiler_chat_form", clear_on_submit=True):
                c_input_col, c_send_col = st.columns([5, 1])
                with c_input_col:
                    user_msg = st.text_input(
                        "msg",
                        placeholder="Ask about logic, approach, or algorithm…",
                        key="chat_msg_input",
                        label_visibility="collapsed",
                    )
                with c_send_col:
                    send = st.form_submit_button("➤", use_container_width=True)

            if send and user_msg.strip():
                st.session_state.chat_history.append(
                    {"role": "user", "content": user_msg}
                )
                from utils.groq_client import call_groq
                _system = """You are LogicAI Mentor — an expert coding tutor.
Rules:
1. NEVER write complete code solutions or functions.
2. Guide the user's thinking with questions and conceptual explanations.
3. Explain logic, patterns, and algorithms at a conceptual level.
4. If asked for code, respond with pseudocode or steps only.
5. Be concise (3–5 sentences). Use simple markdown formatting."""
                _prompt = (
                    f"User's code ({st.session_state.editor_language}):\n"
                    f"```\n{st.session_state.editor_code}\n```\n\n"
                    f"User question: {user_msg}"
                )
                with st.spinner("🧠 Thinking…"):
                    _resp = call_groq(_system, _prompt)
                st.session_state.chat_history.append({"role": "ai", "content": _resp})
                st.rerun()

            st.markdown("</div>", unsafe_allow_html=True)  # close lai-chat-panel


# ─── MAIN ────────────────────────────────────────────────────────────────────
render_top_nav()

active = st.session_state.active_page

if active == "compiler":
    render_compiler_page()
elif active == "debugger":
    debugger.render()
elif active == "visualizer":
    visualizer.render()
elif active == "optimizer":
    optimizer.render()
elif active == "logic":
    logic_engine.render()
elif active == "pathfinder":
    pathfinder.render()

# ─── JS INJECTION (runs in iframe → accesses window.parent) ─────────────────
components.html(
    f"""
{_RESIZE_JS}
<script>
    // Pass active page to resize script
    window.parent.__LAI_ACTIVE = '{active}';
</script>
""",
    height=0,
)
