import streamlit as st

def inject_css():
    st.markdown("""
    <style>
    /* ===== IMPORT FONTS ===== */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');

    /* ===== ROOT VARIABLES ===== */
    :root {
        --bg-primary: #0a0d16;
        --bg-secondary: #111827;
        --bg-card: rgba(17, 24, 39, 0.8);
        --bg-glass: rgba(99, 102, 241, 0.05);
        --border-glass: rgba(99, 102, 241, 0.15);
        --accent-indigo: #6366f1;
        --accent-cyan: #22d3ee;
        --accent-amber: #f59e0b;
        --accent-green: #10b981;
        --accent-red: #ef4444;
        --text-primary: #e2e8f0;
        --text-secondary: #94a3b8;
        --text-muted: #64748b;
        --gradient-hero: linear-gradient(135deg, #6366f1 0%, #22d3ee 100%);
        --gradient-card: linear-gradient(135deg, rgba(99,102,241,0.1) 0%, rgba(34,211,238,0.05) 100%);
        --shadow-glow: 0 0 30px rgba(99, 102, 241, 0.15);
        --shadow-card: 0 4px 24px rgba(0, 0, 0, 0.4);
        --radius-lg: 16px;
        --radius-md: 12px;
        --radius-sm: 8px;
    }

    /* ===== GLOBAL RESET ===== */
    * { box-sizing: border-box; }

    html, body, [data-testid="stAppViewContainer"] {
        background-color: var(--bg-primary) !important;
        font-family: 'Inter', sans-serif;
        color: var(--text-primary);
    }

    [data-testid="stAppViewContainer"] {
        background: radial-gradient(ellipse at top left, rgba(99,102,241,0.08) 0%, transparent 50%),
                    radial-gradient(ellipse at bottom right, rgba(34,211,238,0.05) 0%, transparent 50%),
                    var(--bg-primary) !important;
    }

    /* ===== HIDE STREAMLIT DEFAULTS ===== */
    #MainMenu, footer, [data-testid="stToolbar"] { display: none !important; }
    [data-testid="stDecoration"] { display: none !important; }
    [data-testid="collapsedControl"] { display: none !important; }

    /* ===== SIDEBAR ===== */
    [data-testid="stSidebar"] {
        background: var(--bg-secondary) !important;
        border-right: 1px solid var(--border-glass) !important;
        box-shadow: 4px 0 24px rgba(0,0,0,0.3);
    }
    [data-testid="stSidebar"] > div { padding-top: 1rem; }

    /* ===== LOGO HEADER ===== */
    .logicpilot-logo {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 8px 0 20px 0;
        border-bottom: 1px solid var(--border-glass);
        margin-bottom: 20px;
    }
    .logicpilot-logo .logo-icon {
        width: 38px;
        height: 38px;
        background: var(--gradient-hero);
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 20px;
        box-shadow: 0 0 16px rgba(99,102,241,0.5);
    }
    .logicpilot-logo .logo-text {
        font-size: 20px;
        font-weight: 700;
        background: var(--gradient-hero);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        letter-spacing: -0.5px;
    }
    .logicpilot-logo .logo-tagline {
        font-size: 10px;
        color: var(--text-muted);
        font-weight: 400;
        letter-spacing: 0.5px;
    }

    /* ===== MODULE NAV BUTTONS ===== */
    .module-nav-btn {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 12px 14px;
        border-radius: var(--radius-sm);
        cursor: pointer;
        transition: all 0.2s ease;
        margin-bottom: 4px;
        border: 1px solid transparent;
        font-size: 13px;
        font-weight: 500;
        color: var(--text-secondary);
        background: transparent;
        width: 100%;
        text-align: left;
    }
    .module-nav-btn:hover {
        background: var(--bg-glass);
        border-color: var(--border-glass);
        color: var(--text-primary);
    }
    .module-nav-btn.active {
        background: linear-gradient(135deg, rgba(99,102,241,0.2), rgba(34,211,238,0.1));
        border-color: var(--accent-indigo);
        color: var(--accent-indigo);
        box-shadow: 0 0 12px rgba(99,102,241,0.15);
    }

    /* ===== CARDS ===== */
    .glass-card {
        background: var(--bg-glass);
        border: 1px solid var(--border-glass);
        border-radius: var(--radius-lg);
        padding: 20px;
        backdrop-filter: blur(10px);
        box-shadow: var(--shadow-card);
        margin-bottom: 16px;
    }
    .glass-card h3 {
        color: var(--text-primary);
        font-size: 15px;
        font-weight: 600;
        margin: 0 0 12px 0;
    }

    /* ===== MODULE HEADER ===== */
    .module-header {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 16px 0 20px 0;
        border-bottom: 1px solid var(--border-glass);
        margin-bottom: 20px;
    }
    .module-header .module-icon {
        font-size: 28px;
    }
    .module-header h1 {
        font-size: 22px;
        font-weight: 700;
        margin: 0;
        background: var(--gradient-hero);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .module-header p {
        font-size: 12px;
        color: var(--text-muted);
        margin: 2px 0 0 0;
    }

    /* ===== AI RESPONSE CARDS ===== */
    .ai-response {
        background: linear-gradient(135deg, rgba(99,102,241,0.08), rgba(34,211,238,0.04));
        border: 1px solid var(--border-glass);
        border-left: 3px solid var(--accent-indigo);
        border-radius: var(--radius-md);
        padding: 16px 18px;
        margin: 12px 0;
        font-size: 14px;
        line-height: 1.7;
        color: var(--text-primary);
    }
    .ai-response .ai-label {
        font-size: 11px;
        font-weight: 600;
        color: var(--accent-indigo);
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        gap: 6px;
    }

    .user-message {
        background: rgba(34,211,238,0.06);
        border: 1px solid rgba(34,211,238,0.15);
        border-left: 3px solid var(--accent-cyan);
        border-radius: var(--radius-md);
        padding: 12px 16px;
        margin: 8px 0;
        font-size: 13px;
        color: var(--text-primary);
    }
    .user-message .user-label {
        font-size: 11px;
        font-weight: 600;
        color: var(--accent-cyan);
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-bottom: 6px;
    }

    /* ===== GAP BADGES ===== */
    .badge {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        padding: 4px 10px;
        border-radius: 999px;
        font-size: 11px;
        font-weight: 600;
        margin: 4px 4px 4px 0;
    }
    .badge-green { background: rgba(16,185,129,0.15); color: #10b981; border: 1px solid rgba(16,185,129,0.3); }
    .badge-amber { background: rgba(245,158,11,0.15); color: #f59e0b; border: 1px solid rgba(245,158,11,0.3); }
    .badge-red   { background: rgba(239,68,68,0.15);  color: #ef4444; border: 1px solid rgba(239,68,68,0.3);  }
    .badge-blue  { background: rgba(99,102,241,0.15); color: #6366f1; border: 1px solid rgba(99,102,241,0.3); }

    /* ===== STEP CARDS ===== */
    .step-card {
        border: 1px solid var(--border-glass);
        border-radius: var(--radius-md);
        overflow: hidden;
        margin-bottom: 10px;
        transition: all 0.3s ease;
    }
    .step-card.locked {
        opacity: 0.5;
    }
    .step-card.completed {
        border-color: rgba(16,185,129,0.4);
        background: rgba(16,185,129,0.04);
    }
    .step-header {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 14px 16px;
        cursor: pointer;
    }
    .step-number {
        width: 28px;
        height: 28px;
        border-radius: 50%;
        background: var(--accent-indigo);
        color: white;
        font-size: 13px;
        font-weight: 700;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
    }
    .step-number.locked-num { background: var(--text-muted); }
    .step-number.done-num { background: var(--accent-green); }

    /* ===== COMPLEXITY TABLE ===== */
    .complexity-table {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1px;
        background: var(--border-glass);
        border-radius: var(--radius-md);
        overflow: hidden;
        margin: 16px 0;
    }
    .complexity-col {
        background: var(--bg-secondary);
        padding: 16px;
    }
    .complexity-col.optimized { background: rgba(99,102,241,0.08); }
    .complexity-col h4 {
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin: 0 0 12px 0;
    }
    .complexity-col.yours h4 { color: var(--accent-amber); }
    .complexity-col.optimized h4 { color: var(--accent-indigo); }
    .complexity-row {
        display: flex;
        justify-content: space-between;
        padding: 6px 0;
        border-bottom: 1px solid var(--border-glass);
        font-size: 13px;
    }
    .complexity-row:last-child { border-bottom: none; }
    .complexity-label { color: var(--text-muted); }
    .complexity-value { color: var(--text-primary); font-weight: 500; font-family: 'JetBrains Mono', monospace; }

    /* ===== VARIABLE STATE TABLE ===== */
    .var-table {
        font-family: 'JetBrains Mono', monospace;
        font-size: 12px;
        width: 100%;
        border-collapse: collapse;
    }
    .var-table th {
        background: rgba(99,102,241,0.15);
        color: var(--accent-indigo);
        padding: 8px 12px;
        text-align: left;
        font-size: 11px;
        letter-spacing: 0.5px;
    }
    .var-table td {
        padding: 7px 12px;
        border-bottom: 1px solid var(--border-glass);
        color: var(--text-primary);
    }
    .var-table tr:hover td { background: rgba(99,102,241,0.05); }
    .var-changed { color: var(--accent-cyan) !important; font-weight: 600; }

    /* ===== LINE HIGHLIGHT ===== */
    .line-highlight {
        background: rgba(99,102,241,0.15);
        border-left: 3px solid var(--accent-indigo);
        padding: 4px 8px;
        border-radius: 0 4px 4px 0;
        font-family: 'JetBrains Mono', monospace;
        font-size: 13px;
        margin: 2px 0;
    }

    /* ===== DEBUGGING CHAT ===== */
    .debug-question {
        background: rgba(245,158,11,0.08);
        border: 1px solid rgba(245,158,11,0.2);
        border-left: 3px solid var(--accent-amber);
        border-radius: var(--radius-md);
        padding: 14px 16px;
        margin: 10px 0;
        font-size: 14px;
        color: var(--text-primary);
    }
    .debug-question .q-label {
        font-size: 11px;
        font-weight: 700;
        color: var(--accent-amber);
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-bottom: 6px;
    }
    .debug-hint {
        background: rgba(34,211,238,0.06);
        border: 1px solid rgba(34,211,238,0.15);
        border-radius: var(--radius-sm);
        padding: 10px 14px;
        font-size: 12px;
        color: var(--accent-cyan);
        font-family: 'JetBrains Mono', monospace;
        margin-top: 8px;
    }

    /* ===== PROGRESS BAR ===== */
    .progress-bar-wrap {
        background: rgba(99,102,241,0.1);
        border-radius: 999px;
        height: 6px;
        overflow: hidden;
        margin: 8px 0;
    }
    .progress-bar-fill {
        height: 100%;
        background: var(--gradient-hero);
        border-radius: 999px;
        transition: width 0.5s ease;
    }

    /* ===== INFO BOXES ===== */
    .info-box {
        display: flex;
        gap: 10px;
        padding: 12px 14px;
        border-radius: var(--radius-sm);
        font-size: 13px;
        margin: 8px 0;
        line-height: 1.5;
        align-items: flex-start;
    }
    .info-box.philosophy {
        background: rgba(99,102,241,0.08);
        border: 1px solid rgba(99,102,241,0.2);
        color: var(--text-secondary);
        font-style: italic;
    }
    .info-box.tip {
        background: rgba(16,185,129,0.08);
        border: 1px solid rgba(16,185,129,0.2);
        color: var(--text-primary);
    }
    .info-box.warning {
        background: rgba(245,158,11,0.08);
        border: 1px solid rgba(245,158,11,0.2);
        color: var(--text-primary);
    }

    /* ===== BUTTONS ===== */
    .stButton > button {
        background: linear-gradient(135deg, #6366f1, #4f46e5) !important;
        color: white !important;
        border: none !important;
        border-radius: var(--radius-sm) !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        font-size: 13px !important;
        padding: 10px 20px !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 4px 14px rgba(99,102,241,0.3) !important;
    }
    .stButton > button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 20px rgba(99,102,241,0.4) !important;
    }
    .stButton > button:active { transform: translateY(0) !important; }

    /* ===== TEXT INPUTS ===== */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background: var(--bg-secondary) !important;
        border: 1px solid var(--border-glass) !important;
        border-radius: var(--radius-sm) !important;
        color: var(--text-primary) !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 14px !important;
    }
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: var(--accent-indigo) !important;
        box-shadow: 0 0 0 2px rgba(99,102,241,0.2) !important;
    }

    /* ===== SELECTBOX ===== */
    .stSelectbox > div > div {
        background: var(--bg-secondary) !important;
        border: 1px solid var(--border-glass) !important;
        border-radius: var(--radius-sm) !important;
        color: var(--text-primary) !important;
    }

    /* ===== DIVIDER ===== */
    hr { border-color: var(--border-glass) !important; margin: 16px 0; }

    /* ===== EXPANDER ===== */
    [data-testid="stExpander"] {
        background: var(--bg-glass) !important;
        border: 1px solid var(--border-glass) !important;
        border-radius: var(--radius-md) !important;
    }
    [data-testid="stExpander"] summary {
        color: var(--text-primary) !important;
        font-weight: 500;
    }

    /* ===== CODE BLOCK ===== */
    code {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 12px !important;
        background: rgba(99,102,241,0.1) !important;
        color: var(--accent-cyan) !important;
        padding: 2px 6px !important;
        border-radius: 4px !important;
    }
    pre code {
        background: transparent !important;
        padding: 0 !important;
    }

    /* ===== SCROLLBAR ===== */
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: var(--border-glass); border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: var(--accent-indigo); }

    /* ===== METRIC CARDS ===== */
    [data-testid="stMetric"] {
        background: var(--bg-glass) !important;
        border: 1px solid var(--border-glass) !important;
        border-radius: var(--radius-md) !important;
        padding: 12px 16px !important;
    }
    [data-testid="stMetricValue"] { color: var(--accent-indigo) !important; }

    /* ===== RADIO ===== */
    .stRadio > div { gap: 8px; }
    .stRadio label {
        background: var(--bg-secondary) !important;
        border: 1px solid var(--border-glass) !important;
        border-radius: var(--radius-sm) !important;
        padding: 6px 14px !important;
        cursor: pointer !important;
        transition: all 0.2s;
        color: var(--text-secondary) !important;
        font-size: 13px !important;
    }

    /* ===== SECTION DIVIDERS ===== */
    .section-title {
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        color: var(--text-muted);
        margin: 16px 0 8px 0;
        padding-left: 2px;
    }

    /* ===== CHAT AREA ===== */
    .chat-container {
        max-height: 450px;
        overflow-y: auto;
        padding: 4px;
    }

    /* ===== COMPLEXITY METER BARS ===== */
    .complexity-meter {
        margin: 8px 0;
    }
    .complexity-meter .label {
        font-size: 12px;
        color: var(--text-muted);
        margin-bottom: 4px;
    }
    .complexity-meter .bar-bg {
        background: rgba(255,255,255,0.05);
        border-radius: 4px;
        height: 8px;
        overflow: hidden;
    }
    .complexity-meter .bar-fill {
        height: 100%;
        border-radius: 4px;
        transition: width 1s ease;
    }
    .bar-danger { background: linear-gradient(90deg, #ef4444, #f59e0b); }
    .bar-success { background: linear-gradient(90deg, #10b981, #22d3ee); }

    /* ===== MAIN CONTENT AREA ===== */
    .main-content { padding: 0 8px; }

    /* ===== API KEY INPUT ===== */
    .api-key-section {
        background: rgba(99,102,241,0.06);
        border: 1px solid var(--border-glass);
        border-radius: var(--radius-md);
        padding: 14px;
        margin-bottom: 16px;
    }
    .api-key-section .key-label {
        font-size: 11px;
        font-weight: 600;
        color: var(--accent-indigo);
        letter-spacing: 0.5px;
        margin-bottom: 8px;
    }

    /* ===== FOOTER ===== */
    .sidebar-footer {
        position: absolute;
        bottom: 16px;
        left: 16px;
        right: 16px;
        text-align: center;
        font-size: 11px;
        color: var(--text-muted);
        border-top: 1px solid var(--border-glass);
        padding-top: 12px;
    }
    </style>
    """, unsafe_allow_html=True)

def logo_html():
    return """
    <div class="logicpilot-logo">
        <div class="logo-icon">🧠</div>
        <div>
            <div class="logo-text">LogicPilot</div>
            <div class="logo-tagline">AI CODING MENTOR</div>
        </div>
    </div>
    """

def module_header_html(icon: str, title: str, description: str):
    return f"""
    <div class="module-header">
        <span class="module-icon">{icon}</span>
        <div>
            <h1>{title}</h1>
            <p>{description}</p>
        </div>
    </div>
    """

def ai_response_html(text: str, label: str = "🧠 LogicPilot"):
    safe = text.replace("<", "&lt;").replace(">", "&gt;")
    return f"""
    <div class="ai-response">
        <div class="ai-label">{label}</div>
        {safe}
    </div>
    """

def user_message_html(text: str):
    safe = text.replace("<", "&lt;").replace(">", "&gt;")
    return f"""
    <div class="user-message">
        <div class="user-label">👤 You</div>
        {safe}
    </div>
    """

def badge_html(label: str, color: str = "blue"):
    return f'<span class="badge badge-{color}">{label}</span>'

def section_title_html(title: str):
    return f'<div class="section-title">{title}</div>'

def progress_bar_html(percent: int):
    return f"""
    <div class="progress-bar-wrap">
        <div class="progress-bar-fill" style="width:{percent}%"></div>
    </div>
    """

def glass_card_html(content: str, title: str = ""):
    title_html = f"<h3>{title}</h3>" if title else ""
    return f'<div class="glass-card">{title_html}{content}</div>'

def complexity_meter_html(label: str, value_label: str, percent: int, danger: bool = False):
    bar_class = "bar-danger" if danger else "bar-success"
    return f"""
    <div class="complexity-meter">
        <div class="label">{label} — <strong>{value_label}</strong></div>
        <div class="bar-bg"><div class="bar-fill {bar_class}" style="width:{percent}%"></div></div>
    </div>
    """

def debug_question_html(question: str, hint: str = ""):
    hint_html = f'<div class="debug-hint">💡 Hint: {hint}</div>' if hint else ""
    return f"""
    <div class="debug-question">
        <div class="q-label">🤔 Socratic Question</div>
        {question}
        {hint_html}
    </div>
    """
