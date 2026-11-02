import streamlit as st

def stat_card(title, value):
    st.markdown(f"""
    <div class="stat-card">
        <h2>{value}</h2>
        <p>{title}</p>
    </div>
    """, unsafe_allow_html=True)

def notice_card(title, content, date, category):
    st.markdown(f"""
    <div class="card">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <h3 style="margin: 0;">{title}</h3>
            <span class="category-badge">{category}</span>
        </div>
        <p style="color: var(--text-muted, #94a3b8); font-size: 0.82rem; margin-top: 6px; font-weight: 500;">{date}</p>
        <p style="margin-top: 10px; color: var(--text-primary, #1e293b); line-height: 1.6;">{content}</p>
    </div>
    """, unsafe_allow_html=True)
