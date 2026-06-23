import streamlit as st


# ──────────────────────────────────────────────────────────────────────────────
# MAIN CSS INJECTION
# ──────────────────────────────────────────────────────────────────────────────
def inject_css():
    st.markdown(
        """
<style>
/* ── FONTS ──────────────────────────────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

/* ── ROOT TOKENS ─────────────────────────────────────────────────────────── */
:root {
    --bg-base:          #050c1a;
    --bg-primary:       #080f1e;
    --bg-secondary:     #0d1428;
    --bg-card:          #111c32;
    --bg-glass:         rgba(139, 92, 246, 0.05);
    --border-subtle:    rgba(139, 92, 246, 0.12);
    --border-mid:       rgba(139, 92, 246, 0.25);
    --border-accent:    rgba(139, 92, 246, 0.45);

    --violet:           #8b5cf6;
    --violet-dim:       rgba(139, 92, 246, 0.55);
    --violet-glow:      rgba(139, 92, 246, 0.25);
    --cyan:             #06b6d4;
    --cyan-dim:         rgba(6, 182, 212, 0.55);
    --emerald:          #10b981;
    --amber:            #f59e0b;
    --rose:             #f43f5e;

    --text-primary:     #f1f5f9;
    --text-secondary:   #94a3b8;
    --text-muted:       #475569;

    --grad-hero:        linear-gradient(135deg, #8b5cf6 0%, #06b6d4 100%);
    --grad-card:        linear-gradient(135deg, rgba(139,92,246,0.08), rgba(6,182,212,0.04));
    --grad-border:      linear-gradient(135deg, rgba(139,92,246,0.4), rgba(6,182,212,0.2));

    --shadow-sm:        0 2px 8px rgba(0,0,0,0.3);
    --shadow-md:        0 4px 20px rgba(0,0,0,0.45);
    --shadow-lg:        0 8px 40px rgba(0,0,0,0.55);
    --glow-violet:      0 0 24px rgba(139,92,246,0.3);
    --glow-cyan:        0 0 24px rgba(6,182,212,0.25);

    --radius-xl:  16px;
    --radius-lg:  12px;
    --radius-md:  8px;
    --radius-sm:  6px;
}

/* ── GLOBAL RESET ─────────────────────────────────────────────────────────── */
*, *::before, *::after { box-sizing: border-box; }

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewBlockContainer"] {
    background: var(--bg-base) !important;
    font-family: 'Inter', system-ui, sans-serif;
    color: var(--text-primary);
    min-height: 100vh;
    padding: 0 !important;
    margin: 0 !important;
    max-width: 100% !important;
}

/* ── HIDE STREAMLIT CHROME ────────────────────────────────────────────────── */
#MainMenu, footer,
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stSidebar"],
[data-testid="collapsedControl"],
section[data-testid="stSidebarContent"] {
    display: none !important;
}

/* ── CONTENT CONTAINER ───────────────────────────────────────────────────── */
.main .block-container {
    padding: 0 !important;
    margin: 0 !important;
    max-width: 100% !important;
    width: 100% !important;
}
section.main {
    padding-top: 0 !important;
}

/* ── SCROLLBAR ───────────────────────────────────────────────────────────── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: var(--bg-primary); }
::-webkit-scrollbar-thumb {
    background: var(--violet-dim);
    border-radius: 3px;
}
::-webkit-scrollbar-thumb:hover { background: var(--violet); }

/* ═══════════════════════════════════════════════════════════════════════════
   LOGO + HEADER BAR
═══════════════════════════════════════════════════════════════════════════ */
.lai-header {
    display: flex;
    align-items: center;
    gap: 0;
    padding: 0 24px;
    height: 64px;
    background: var(--bg-secondary);
    border-bottom: 1px solid var(--border-subtle);
    position: sticky;
    top: 0;
    z-index: 200;
    box-shadow: var(--shadow-md);
}

.lai-logo-wrap {
    display: flex;
    align-items: center;
    gap: 10px;
    padding-right: 24px;
    border-right: 1px solid var(--border-subtle);
    margin-right: 16px;
    flex-shrink: 0;
}

.lai-logo-icon {
    width: 38px;
    height: 38px;
    background: var(--grad-hero);
    border-radius: var(--radius-md);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    box-shadow: var(--glow-violet);
}

.lai-logo-text {
    line-height: 1.2;
}

.lai-logo-name {
    font-size: 17px;
    font-weight: 800;
    background: var(--grad-hero);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: -0.5px;
}

.lai-logo-sub {
    font-size: 9px;
    font-weight: 600;
    letter-spacing: 1.5px;
    color: var(--text-muted);
    text-transform: uppercase;
}

/* ── SECTION DIVIDER AFTER HEADER ───────────────────────────────────────── */
.lai-nav-divider {
    height: 1px;
    background: var(--border-subtle);
    margin: 0;
}

/* ── NAV BUTTONS CONTAINER ───────────────────────────────────────────────── */
.lai-nav-strip {
    background: var(--bg-secondary);
    padding: 8px 24px;
    display: flex;
    align-items: center;
    gap: 6px;
    border-bottom: 1px solid var(--border-subtle);
    flex-wrap: nowrap;
}

/* Style all buttons inside nav strip */
[data-testid="stHorizontalBlock"]:first-of-type [data-testid="stButton"] button {
    height: 38px !important;
    padding: 0 16px !important;
    border-radius: var(--radius-md) !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    letter-spacing: 0.2px !important;
    border: 1px solid var(--border-subtle) !important;
    background: transparent !important;
    color: var(--text-secondary) !important;
    transition: all 0.2s ease !important;
    white-space: nowrap !important;
    box-shadow: none !important;
}

[data-testid="stHorizontalBlock"]:first-of-type [data-testid="stButton"] button:hover {
    background: var(--bg-glass) !important;
    border-color: var(--border-mid) !important;
    color: var(--text-primary) !important;
    transform: translateY(-1px) !important;
    box-shadow: var(--shadow-sm) !important;
}

/* Active nav button - set via JS class */
.lai-nav-active button {
    background: var(--grad-hero) !important;
    border-color: transparent !important;
    color: white !important;
    box-shadow: 0 4px 15px rgba(139,92,246,0.4) !important;
}

/* ═══════════════════════════════════════════════════════════════════════════
   COMPILER PAGE — PANELS
═══════════════════════════════════════════════════════════════════════════ */

/* Editor column */
.lai-editor-col {
    background: var(--bg-primary);
    border-right: 1px solid var(--border-subtle);
    min-height: calc(100vh - 120px);
    padding: 16px;
}

/* Right panel (chatbot + output) */
.lai-right-col {
    background: var(--bg-primary);
    display: flex;
    flex-direction: column;
    min-height: calc(100vh - 120px);
}

/* Panel header label */
.lai-panel-header {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 10px 16px;
    background: var(--bg-secondary);
    border-bottom: 1px solid var(--border-subtle);
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
    color: var(--violet);
}

.lai-panel-header .panel-dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: var(--grad-hero);
    box-shadow: var(--glow-violet);
}

/* Vertical resize handle between chatbot and output */
.lai-v-handle {
    height: 8px;
    cursor: row-resize;
    background: linear-gradient(90deg, var(--violet-glow), var(--cyan-dim), var(--violet-glow));
    border-radius: 4px;
    margin: 0;
    flex-shrink: 0;
    transition: background 0.2s, height 0.1s;
}
.lai-v-handle:hover {
    height: 10px;
    background: var(--grad-hero);
}

/* Horizontal resize handle between left/right columns */
.lai-resize-h {
    cursor: col-resize;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    transition: background 0.2s;
    border-radius: 4px;
}
.lai-resize-h .lai-h-pill {
    width: 4px;
    height: 60px;
    background: linear-gradient(180deg, var(--violet-glow), var(--cyan-dim));
    border-radius: 2px;
    transition: all 0.2s;
}
.lai-resize-h:hover .lai-h-pill {
    background: var(--grad-hero);
    box-shadow: var(--glow-violet);
    height: 80px;
}

/* ═══════════════════════════════════════════════════════════════════════════
   CHAT MESSAGES
═══════════════════════════════════════════════════════════════════════════ */
.chat-scroll {
    max-height: 320px;
    overflow-y: auto;
    padding: 8px 16px;
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.chat-bubble-user {
    align-self: flex-end;
    max-width: 82%;
    background: var(--grad-hero);
    color: white;
    padding: 10px 14px;
    border-radius: var(--radius-lg) var(--radius-sm) var(--radius-lg) var(--radius-lg);
    font-size: 13px;
    line-height: 1.5;
    box-shadow: 0 4px 12px rgba(139,92,246,0.35);
}

.chat-bubble-ai {
    align-self: flex-start;
    max-width: 88%;
    background: var(--bg-card);
    color: var(--text-primary);
    padding: 12px 14px;
    border-radius: var(--radius-sm) var(--radius-lg) var(--radius-lg) var(--radius-lg);
    border: 1px solid var(--border-subtle);
    font-size: 13px;
    line-height: 1.65;
    box-shadow: var(--shadow-sm);
}

.chat-bubble-ai .ai-label {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1px;
    color: var(--violet);
    text-transform: uppercase;
    margin-bottom: 6px;
}

/* Typing indicator */
@keyframes bounce {
    0%, 80%, 100% { transform: translateY(0); }
    40%           { transform: translateY(-6px); }
}
.typing-dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: var(--violet);
    display: inline-block;
    margin: 0 2px;
    animation: bounce 1.2s infinite;
}
.typing-dot:nth-child(2) { animation-delay: 0.15s; }
.typing-dot:nth-child(3) { animation-delay: 0.3s; }

/* ═══════════════════════════════════════════════════════════════════════════
   OUTPUT SCREEN
═══════════════════════════════════════════════════════════════════════════ */
.lai-output-area {
    flex: 1;
    padding: 12px 16px;
    background: var(--bg-primary);
    overflow-y: auto;
    font-family: 'JetBrains Mono', monospace;
    font-size: 13px;
    color: var(--emerald);
    white-space: pre-wrap;
    word-break: break-word;
    min-height: 120px;
}

.lai-output-error {
    color: var(--rose);
    background: rgba(244,63,94,0.06);
    border: 1px solid rgba(244,63,94,0.2);
    border-radius: var(--radius-md);
    padding: 12px 14px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px;
    white-space: pre-wrap;
    margin-top: 8px;
}

.lai-output-empty {
    color: var(--text-muted);
    font-size: 12px;
    font-family: 'Inter', sans-serif;
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 16px 0;
}

/* ═══════════════════════════════════════════════════════════════════════════
   GLASS CARDS
═══════════════════════════════════════════════════════════════════════════ */
.glass-card {
    background: var(--bg-glass);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-lg);
    padding: 18px;
    backdrop-filter: blur(12px);
    box-shadow: var(--shadow-md);
    margin-bottom: 14px;
    position: relative;
    overflow: hidden;
}
.glass-card::before {
    content: '';
    position: absolute;
    inset: 0;
    border-radius: inherit;
    background: var(--grad-card);
    z-index: 0;
    pointer-events: none;
}
.glass-card > * { position: relative; z-index: 1; }
.glass-card h3 {
    font-size: 14px;
    font-weight: 700;
    color: var(--text-primary);
    margin: 0 0 12px 0;
}

/* ═══════════════════════════════════════════════════════════════════════════
   MODULE HEADERS
═══════════════════════════════════════════════════════════════════════════ */
.module-header {
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 20px 24px;
    border-bottom: 1px solid var(--border-subtle);
    background: var(--bg-secondary);
    margin-bottom: 0;
}
.module-header .mod-icon {
    width: 46px;
    height: 46px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 22px;
    background: var(--bg-card);
    border: 1px solid var(--border-mid);
    border-radius: var(--radius-md);
    box-shadow: var(--glow-violet);
    flex-shrink: 0;
}
.module-header h1 {
    font-size: 20px;
    font-weight: 800;
    margin: 0;
    background: var(--grad-hero);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.module-header p {
    font-size: 12px;
    color: var(--text-muted);
    margin: 3px 0 0;
}

/* ── SECTION TITLES ─────────────────────────────────────────────────────── */
.section-title {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--violet);
    margin: 16px 0 8px;
    display: flex;
    align-items: center;
    gap: 8px;
}
.section-title::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border-subtle);
}

/* ═══════════════════════════════════════════════════════════════════════════
   CODE DISPLAY (read-only mirrors)
═══════════════════════════════════════════════════════════════════════════ */
.code-mirror {
    background: #0d1117;
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-md);
    font-family: 'JetBrains Mono', monospace;
    font-size: 12.5px;
    line-height: 1.65;
    color: #e2e8f0;
    padding: 14px;
    overflow-y: auto;
    white-space: pre-wrap;
    word-break: break-word;
    counter-reset: line-num;
}

/* Line highlight for visualizer/debugger */
.line-active {
    background: rgba(139,92,246,0.18);
    border-left: 3px solid var(--violet);
    border-radius: 0 4px 4px 0;
    padding: 3px 8px;
    margin: 2px 0;
    font-family: 'JetBrains Mono', monospace;
    font-size: 13px;
    color: var(--text-primary);
}

.line-inactive {
    padding: 2px 8px;
    color: var(--text-muted);
    font-family: 'JetBrains Mono', monospace;
    font-size: 13px;
}

/* ═══════════════════════════════════════════════════════════════════════════
   AI RESPONSE CARDS
═══════════════════════════════════════════════════════════════════════════ */
.ai-response {
    background: rgba(139,92,246,0.05);
    border: 1px solid var(--border-subtle);
    border-left: 3px solid var(--violet);
    border-radius: var(--radius-md);
    padding: 14px 16px;
    margin: 10px 0;
    font-size: 13.5px;
    line-height: 1.7;
    color: var(--text-primary);
}
.ai-response .ai-label {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: var(--violet);
    margin-bottom: 8px;
    display: flex;
    align-items: center;
    gap: 6px;
}

.user-message {
    background: rgba(255,255,255,0.02);
    border: 1px solid var(--border-subtle);
    border-left: 3px solid var(--text-muted);
    border-radius: var(--radius-md);
    padding: 12px 16px;
    margin: 8px 0;
    font-size: 13px;
    color: var(--text-primary);
}
.user-message .user-label {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
    color: var(--text-muted);
    margin-bottom: 6px;
}

/* ── DEBUGGER QUESTION BUBBLES ─────────────────────────────────────────── */
.debug-question {
    background: rgba(245,158,11,0.07);
    border: 1px solid rgba(245,158,11,0.2);
    border-left: 3px solid var(--amber);
    border-radius: var(--radius-md);
    padding: 14px 16px;
    margin: 10px 0;
    font-size: 13.5px;
    line-height: 1.7;
    color: var(--text-primary);
}
.debug-question .q-label {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
    color: var(--amber);
    margin-bottom: 6px;
}
.debug-hint {
    background: rgba(6,182,212,0.08);
    border: 1px solid rgba(6,182,212,0.2);
    border-radius: var(--radius-sm);
    padding: 8px 12px;
    font-size: 12px;
    color: var(--cyan);
    font-family: 'JetBrains Mono', monospace;
    margin-top: 8px;
}

/* ═══════════════════════════════════════════════════════════════════════════
   BADGES
═══════════════════════════════════════════════════════════════════════════ */
.badge {
    display: inline-flex; align-items: center; gap: 4px;
    padding: 3px 10px; border-radius: 999px;
    font-size: 11px; font-weight: 600; margin: 3px 3px 3px 0;
}
.badge-violet  { background: rgba(139,92,246,0.15);  color: var(--violet);  border: 1px solid rgba(139,92,246,0.3);  }
.badge-cyan    { background: rgba(6,182,212,0.15);   color: var(--cyan);    border: 1px solid rgba(6,182,212,0.3);   }
.badge-emerald { background: rgba(16,185,129,0.15);  color: var(--emerald); border: 1px solid rgba(16,185,129,0.3); }
.badge-amber   { background: rgba(245,158,11,0.15);  color: var(--amber);   border: 1px solid rgba(245,158,11,0.3);  }
.badge-rose    { background: rgba(244,63,94,0.15);   color: var(--rose);    border: 1px solid rgba(244,63,94,0.3);   }

/* ═══════════════════════════════════════════════════════════════════════════
   PROGRESS BAR
═══════════════════════════════════════════════════════════════════════════ */
.progress-track {
    background: rgba(139,92,246,0.1);
    border-radius: 999px;
    height: 5px;
    overflow: hidden;
    margin: 6px 0;
}
.progress-fill {
    height: 100%;
    background: var(--grad-hero);
    border-radius: 999px;
    transition: width 0.5s ease;
}

/* ═══════════════════════════════════════════════════════════════════════════
   INFO BOXES
═══════════════════════════════════════════════════════════════════════════ */
.info-box {
    display: flex; gap: 10px;
    padding: 12px 14px;
    border-radius: var(--radius-sm);
    font-size: 13px;
    margin: 8px 0;
    line-height: 1.55;
    align-items: flex-start;
}
.info-box.philosophy {
    background: rgba(6,182,212,0.05);
    border: 1px solid rgba(6,182,212,0.15);
    color: var(--text-secondary);
    font-style: italic;
}
.info-box.tip {
    background: rgba(16,185,129,0.05);
    border: 1px solid rgba(16,185,129,0.2);
    color: var(--text-primary);
}
.info-box.warning {
    background: rgba(245,158,11,0.05);
    border: 1px solid rgba(245,158,11,0.2);
    color: var(--text-primary);
}

/* ═══════════════════════════════════════════════════════════════════════════
   COMPLEXITY TABLE
═══════════════════════════════════════════════════════════════════════════ */
.complexity-meter { margin: 8px 0; }
.complexity-meter .c-label {
    font-size: 12px; color: var(--text-muted); margin-bottom: 4px;
}
.complexity-meter .c-bar-bg {
    background: rgba(255,255,255,0.05);
    border-radius: 4px; height: 7px; overflow: hidden;
}
.complexity-meter .c-bar-fill { height: 100%; border-radius: 4px; }
.bar-danger  { background: linear-gradient(90deg, var(--rose), var(--amber)); }
.bar-success { background: linear-gradient(90deg, var(--emerald), var(--cyan)); }

.var-table {
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px; width: 100%; border-collapse: collapse;
}
.var-table th {
    background: rgba(139,92,246,0.12);
    color: var(--violet);
    padding: 8px 12px;
    text-align: left; font-size: 10px; letter-spacing: 0.5px;
}
.var-table td {
    padding: 7px 12px;
    border-bottom: 1px solid var(--border-subtle);
    color: var(--text-primary);
}
.var-table tr:hover td { background: rgba(139,92,246,0.05); }
.var-changed { color: var(--cyan) !important; font-weight: 600; }

/* ═══════════════════════════════════════════════════════════════════════════
   STREAMLIT WIDGET OVERRIDES
═══════════════════════════════════════════════════════════════════════════ */

/* Buttons */
.stButton > button {
    background: var(--bg-card) !important;
    color: var(--text-primary) !important;
    border: 1px solid var(--border-mid) !important;
    border-radius: var(--radius-md) !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    padding: 8px 18px !important;
    transition: all 0.2s ease !important;
    box-shadow: none !important;
}
.stButton > button:hover {
    background: var(--bg-glass) !important;
    border-color: var(--border-accent) !important;
    transform: translateY(-1px) !important;
    box-shadow: var(--shadow-sm) !important;
}
.stButton > button[kind="primary"] {
    background: var(--grad-hero) !important;
    border-color: transparent !important;
    color: white !important;
    box-shadow: 0 4px 15px rgba(139,92,246,0.4) !important;
}
.stButton > button[kind="primary"]:hover {
    opacity: 0.92 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(139,92,246,0.5) !important;
}

/* Text inputs */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: var(--bg-secondary) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: var(--radius-md) !important;
    color: var(--text-primary) !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 13.5px !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: var(--violet) !important;
    box-shadow: 0 0 0 3px rgba(139,92,246,0.15) !important;
}

/* Selectbox */
.stSelectbox > div > div {
    background: var(--bg-secondary) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: var(--radius-md) !important;
    color: var(--text-primary) !important;
}
.stSelectbox [data-baseweb="select"] {
    background: var(--bg-secondary) !important;
}

/* Code block */
.stCodeBlock, code {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 12.5px !important;
    background: rgba(139,92,246,0.08) !important;
    color: var(--cyan) !important;
    border-radius: 4px !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: var(--bg-secondary) !important;
    border-bottom: 1px solid var(--border-subtle) !important;
    gap: 0 !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: var(--text-muted) !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    padding: 10px 18px !important;
    border-bottom: 2px solid transparent !important;
    transition: all 0.2s !important;
}
.stTabs [aria-selected="true"] {
    color: var(--violet) !important;
    border-bottom-color: var(--violet) !important;
    background: transparent !important;
}

/* Expander */
[data-testid="stExpander"] {
    background: var(--bg-glass) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: var(--radius-md) !important;
}
[data-testid="stExpander"] summary { color: var(--text-primary) !important; font-weight: 500; }

/* Divider */
hr { border-color: var(--border-subtle) !important; margin: 14px 0 !important; }

/* Metrics */
[data-testid="stMetric"] {
    background: var(--bg-glass) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: var(--radius-md) !important;
    padding: 12px 16px !important;
}
[data-testid="stMetricValue"] { color: var(--violet) !important; }

/* Spinner */
.stSpinner > div { border-top-color: var(--violet) !important; }

/* ═══════════════════════════════════════════════════════════════════════════
   MICRO-ANIMATIONS
═══════════════════════════════════════════════════════════════════════════ */
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(10px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes pulse-glow {
    0%, 100% { box-shadow: 0 0 10px rgba(139,92,246,0.2); }
    50%       { box-shadow: 0 0 25px rgba(139,92,246,0.5); }
}
@keyframes shimmer {
    0%   { background-position: -200% 0; }
    100% { background-position: 200% 0; }
}

.fade-in-up { animation: fadeInUp 0.35s ease-out; }

.lai-run-btn button {
    background: linear-gradient(135deg, var(--emerald), #059669) !important;
    border-color: transparent !important;
    color: white !important;
    box-shadow: 0 4px 15px rgba(16,185,129,0.35) !important;
}
.lai-run-btn button:hover {
    box-shadow: 0 6px 20px rgba(16,185,129,0.5) !important;
}

/* ═══════════════════════════════════════════════════════════════════════════
   OPTIMIZER PAGE
═══════════════════════════════════════════════════════════════════════════ */
.complexity-row {
    display: flex;
    justify-content: space-between;
    padding: 6px 0;
    border-bottom: 1px solid var(--border-subtle);
    font-size: 13px;
}
.complexity-row:last-child { border-bottom: none; }
.complexity-label { color: var(--text-muted); }
.complexity-value {
    color: var(--text-primary);
    font-weight: 500;
    font-family: 'JetBrains Mono', monospace;
}

/* ═══════════════════════════════════════════════════════════════════════════
   STEP CARDS (pathfinder)
═══════════════════════════════════════════════════════════════════════════ */
.step-card {
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-md);
    overflow: hidden;
    margin-bottom: 10px;
    transition: all 0.3s ease;
}
.step-card.completed { border-color: rgba(16,185,129,0.4); background: rgba(16,185,129,0.04); }
.step-card.locked    { opacity: 0.5; }
.step-header {
    display: flex; align-items: center; gap: 12px;
    padding: 14px 16px; cursor: pointer;
}
.step-number {
    width: 28px; height: 28px; border-radius: 50%;
    background: var(--violet); color: white;
    font-size: 13px; font-weight: 700;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0;
}
.step-number.locked-num { background: var(--text-muted); }
.step-number.done-num   { background: var(--emerald); }

/* ═══════════════════════════════════════════════════════════════════════════
   SIDEBAR FOOTER (legacy compat)
═══════════════════════════════════════════════════════════════════════════ */
.sidebar-footer { display: none; }

/* ═══════════════════════════════════════════════════════════════════════════
   LANGUAGE SELECTOR PILL
═══════════════════════════════════════════════════════════════════════════ */
.lang-pill {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    background: rgba(6,182,212,0.12);
    border: 1px solid rgba(6,182,212,0.3);
    color: var(--cyan);
    padding: 3px 10px;
    border-radius: 999px;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}

/* Run button status */
.output-status-ok  { color: var(--emerald); }
.output-status-err { color: var(--rose); }
</style>
""",
        unsafe_allow_html=True,
    )


# ──────────────────────────────────────────────────────────────────────────────
# HTML HELPERS
# ──────────────────────────────────────────────────────────────────────────────

def logo_html() -> str:
    return """
<div class="lai-logo-wrap">
    <div class="lai-logo-icon">🧠</div>
    <div class="lai-logo-text">
        <div class="lai-logo-name">LogicAI</div>
        <div class="lai-logo-sub">Code Intelligence</div>
    </div>
</div>
"""


def module_header_html(icon: str, title: str, description: str) -> str:
    return f"""
<div class="module-header">
    <div class="mod-icon">{icon}</div>
    <div>
        <h1>{title}</h1>
        <p>{description}</p>
    </div>
</div>
"""


def section_title_html(title: str) -> str:
    return f'<div class="section-title">{title}</div>'


def ai_response_html(text: str, label: str = "🧠 LogicAI") -> str:
    safe = text.replace("<", "&lt;").replace(">", "&gt;")
    return f"""
<div class="ai-response">
    <div class="ai-label">{label}</div>
    {safe}
</div>
"""


def user_message_html(text: str) -> str:
    safe = text.replace("<", "&lt;").replace(">", "&gt;")
    return f"""
<div class="user-message">
    <div class="user-label">👤 You</div>
    {safe}
</div>
"""


def badge_html(label: str, color: str = "violet") -> str:
    return f'<span class="badge badge-{color}">{label}</span>'


def progress_bar_html(percent: int) -> str:
    return f"""
<div class="progress-track">
    <div class="progress-fill" style="width:{percent}%"></div>
</div>
"""


def glass_card_html(content: str, title: str = "") -> str:
    t = f"<h3>{title}</h3>" if title else ""
    return f'<div class="glass-card">{t}{content}</div>'


def complexity_meter_html(label: str, value: str, pct: int, danger: bool = False) -> str:
    bar = "bar-danger" if danger else "bar-success"
    return f"""
<div class="complexity-meter">
    <div class="c-label">{label} — <strong>{value}</strong></div>
    <div class="c-bar-bg"><div class="c-bar-fill {bar}" style="width:{pct}%"></div></div>
</div>
"""


def debug_question_html(question: str, hint: str = "") -> str:
    hint_html = f'<div class="debug-hint">💡 {hint}</div>' if hint else ""
    return f"""
<div class="debug-question">
    <div class="q-label">🤔 Socratic Question</div>
    {question}
    {hint_html}
</div>
"""


def panel_header_html(icon: str, title: str) -> str:
    return f"""
<div class="lai-panel-header">
    <span class="panel-dot"></span>
    {icon}&nbsp;{title}
</div>
"""
