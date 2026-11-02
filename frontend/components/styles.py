import streamlit as st

def apply_styles():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    :root {
        --primary: #0f2439;
        --primary-light: #1a3a5c;
        --secondary: #0d9488;
        --secondary-light: #14b8a6;
        --accent: #d97706;
        --accent-light: #f59e0b;
        --bg-light: #f8fafc;
        --bg-white: #ffffff;
        --text-primary: #1e293b;
        --text-secondary: #64748b;
        --text-muted: #94a3b8;
        --border: #e2e8f0;
        --border-light: #f1f5f9;
        --shadow-sm: 0 1px 2px rgba(15, 36, 57, 0.04);
        --shadow-md: 0 4px 12px rgba(15, 36, 57, 0.06);
        --shadow-lg: 0 8px 24px rgba(15, 36, 57, 0.08);
        --shadow-xl: 0 12px 36px rgba(15, 36, 57, 0.10);
        --radius-sm: 6px;
        --radius-md: 10px;
        --radius-lg: 14px;
        --transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .stApp {
        background-color: var(--bg-light);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }

    /* Top navigation bar */
    header[data-testid="stHeader"] {
        background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 100%);
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    }

    /* Main header */
    .main-header {
        color: var(--primary);
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        font-size: 1.75rem;
        letter-spacing: -0.025em;
        line-height: 1.2;
        margin-bottom: 0.25rem;
    }

    .header-divider {
        height: 2px;
        background: linear-gradient(90deg, var(--secondary) 0%, var(--accent) 50%, transparent 100%);
        border: none;
        margin: 0.75rem 0 1.5rem 0;
        border-radius: 1px;
    }

    /* Card base */
    .card {
        background-color: var(--bg-white);
        padding: 1.5rem;
        border-radius: var(--radius-lg);
        box-shadow: var(--shadow-md);
        margin-bottom: 1rem;
        border: 1px solid var(--border-light);
        border-left: 4px solid var(--primary);
        transition: var(--transition);
    }
    .card:hover {
        box-shadow: var(--shadow-lg);
        transform: translateY(-1px);
    }
    .card h3 {
        color: var(--primary);
        margin-top: 0;
        font-weight: 600;
        font-size: 1.1rem;
        letter-spacing: -0.01em;
    }

    /* Stat cards */
    .stat-card {
        background: var(--bg-white);
        padding: 1.25rem 1rem;
        border-radius: var(--radius-md);
        box-shadow: var(--shadow-sm);
        text-align: center;
        position: relative;
        overflow: hidden;
        border: 1px solid var(--border-light);
        transition: var(--transition);
    }
    .stat-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, var(--secondary), var(--accent));
    }
    .stat-card:hover {
        box-shadow: var(--shadow-md);
        transform: translateY(-2px);
    }
    .stat-card h2 {
        color: var(--primary);
        margin: 0.25rem 0 0.15rem 0;
        font-size: 2rem;
        font-weight: 700;
        letter-spacing: -0.02em;
    }
    .stat-card p {
        color: var(--text-secondary);
        margin: 0;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }

    /* Notice category badge */
    .category-badge {
        background: linear-gradient(135deg, var(--secondary), var(--secondary-light));
        color: white;
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 0.02em;
        text-transform: uppercase;
    }

    /* Chat messages */
    .chat-msg {
        padding: 1rem 1.25rem;
        border-radius: var(--radius-md);
        margin-bottom: 0.75rem;
        max-width: 82%;
        font-size: 0.94rem;
        line-height: 1.65;
    }
    .chat-user {
        background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 100%);
        color: #ffffff;
        margin-left: auto;
        border-bottom-right-radius: 3px;
        box-shadow: 0 2px 8px rgba(15, 36, 57, 0.15);
    }
    .chat-assistant {
        background-color: var(--bg-white);
        color: var(--text-primary);
        margin-right: auto;
        border-bottom-left-radius: 3px;
        box-shadow: var(--shadow-md);
        border: 1px solid var(--border);
    }

    /* Source citations */
    .source-doc {
        font-size: 0.76rem;
        background-color: var(--border-light);
        color: var(--text-secondary);
        padding: 4px 10px;
        border-radius: 20px;
        display: inline-block;
        margin-top: 0.5rem;
        margin-right: 0.4rem;
        font-weight: 500;
        border: 1px solid var(--border);
        transition: var(--transition);
    }
    .source-doc:hover {
        background-color: #e2e8f0;
        color: var(--primary);
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, var(--primary) 0%, #0a1a2e 100%);
        border-right: 1px solid rgba(255, 255, 255, 0.06);
    }
    [data-testid="stSidebar"] .stMarkdown h2 {
        color: #ffffff;
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        font-size: 1.2rem;
        letter-spacing: -0.01em;
    }
    [data-testid="stSidebar"] .stMarkdown p,
    [data-testid="stSidebar"] .stMarkdown li {
        color: rgba(255, 255, 255, 0.75);
    }
    [data-testid="stSidebar"] hr {
        border-color: rgba(255, 255, 255, 0.1);
        margin: 0.75rem 0;
    }
    [data-testid="stSidebar"] .stButton > button {
        background: rgba(255, 255, 255, 0.06);
        color: rgba(255, 255, 255, 0.88);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: var(--radius-sm);
        font-weight: 500;
        font-size: 0.88rem;
        padding: 0.55rem 0.75rem;
        transition: var(--transition);
        text-align: left;
    }
    [data-testid="stSidebar"] .stButton > button:hover {
        background: rgba(255, 255, 255, 0.12);
        border-color: rgba(255, 255, 255, 0.18);
        color: #ffffff;
    }
    [data-testid="stSidebar"] .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #dc2626, #b91c1c);
        color: white;
        border: none;
    }
    [data-testid="stSidebar"] .stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, #ef4444, #dc2626);
    }

    /* Form inputs */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div {
        border-radius: var(--radius-sm);
        border: 1.5px solid var(--border);
        font-family: 'Inter', sans-serif;
        font-size: 0.9rem;
        transition: var(--transition);
    }
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: var(--secondary);
        box-shadow: 0 0 0 3px rgba(13, 148, 136, 0.1);
    }

    /* Buttons */
    .stButton > button {
        border-radius: var(--radius-sm);
        font-weight: 500;
        font-family: 'Inter', sans-serif;
        font-size: 0.88rem;
        letter-spacing: 0.01em;
        transition: var(--transition);
        padding: 0.5rem 1.25rem;
    }

    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 6px;
        height: 6px;
    }
    ::-webkit-scrollbar-track {
        background: transparent;
    }
    ::-webkit-scrollbar-thumb {
        background: #cbd5e1;
        border-radius: 3px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #94a3b8;
    }

    /* Smooth animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(6px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .card, .stat-card, .chat-msg {
        animation: fadeIn 0.3s ease-out;
    }

    /* Tables */
    .stDataFrame {
        border-radius: var(--radius-md);
        overflow: hidden;
        box-shadow: var(--shadow-sm);
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.25rem;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: var(--radius-sm) var(--radius-sm) 0 0;
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        font-size: 0.88rem;
    }
    </style>
    """, unsafe_allow_html=True)
