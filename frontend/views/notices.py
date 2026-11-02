import streamlit as st
from utils.api import get
from components.header import render_header
from components.cards import notice_card

def render_notices():
    render_header("Official Notices", "Announcements, examination updates, and administrative circulars")
    
    notices = get("/student/notices")
    
    if notices:
        categories = ["All"] + sorted(list({n.get("category", "General") for n in notices}))
        selected_cat = st.selectbox("Filter by Category", categories)
        
        filtered = notices if selected_cat == "All" else [n for n in notices if n.get("category") == selected_cat]
        
        st.markdown(f"<p style='color: var(--text-secondary); font-size: 0.9rem;'>Showing {len(filtered)} notices</p>", unsafe_allow_html=True)
        
        for notice in filtered:
            notice_card(
                notice.get("title", "No Title"),
                notice.get("content", ""),
                notice.get("date", "Unknown Date"),
                notice.get("category", "General")
            )
    else:
        st.info("No active notices found at this time.")
