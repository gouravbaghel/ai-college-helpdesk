import streamlit as st

def render_header(title, subtitle=None, icon=""):
    st.markdown(f"<h2 class='main-header'>{title}</h2>", unsafe_allow_html=True)
    if subtitle:
        st.markdown(f"<p style='color: var(--text-secondary, #64748b); margin-top: -8px; font-size: 0.95rem;'>{subtitle}</p>", unsafe_allow_html=True)
    st.markdown("<div class='header-divider'></div>", unsafe_allow_html=True)
