import streamlit as st
from utils.session import set_page, logout, is_authenticated

def render_sidebar():
    with st.sidebar:
        st.markdown("## College Helpdesk")
        st.markdown("---")
        
        if not is_authenticated():
            st.info("Please login to access the system.")
            return

        role = st.session_state.role
        
        if role == "student":
            if st.button("Dashboard", use_container_width=True):
                set_page("student_dashboard")
            if st.button("AI Assistant", use_container_width=True):
                set_page("ai_assistant")
            if st.button("Notices", use_container_width=True):
                set_page("notices")
            if st.button("Timetable", use_container_width=True):
                set_page("timetable")
            if st.button("Chat History", use_container_width=True):
                set_page("chat_history")
            if st.button("Profile", use_container_width=True):
                set_page("profile")
        
        elif role == "admin":
            if st.button("Dashboard", use_container_width=True):
                set_page("admin_dashboard")
            if st.button("Documents", use_container_width=True):
                set_page("admin_documents")
            if st.button("Notices", use_container_width=True):
                set_page("admin_notices")
            if st.button("FAQs", use_container_width=True):
                set_page("admin_faqs")
            if st.button("Timetable", use_container_width=True):
                set_page("admin_timetable")
            if st.button("User Queries", use_container_width=True):
                set_page("admin_queries")
            if st.button("Evaluation", use_container_width=True):
                set_page("admin_evaluation")
                
        st.markdown("---")
        if st.button("Logout", use_container_width=True, type="primary"):
            logout()
