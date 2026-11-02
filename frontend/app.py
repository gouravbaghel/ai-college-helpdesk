import streamlit as st
from utils.session import init_session, is_authenticated
from components.styles import apply_styles
from components.sidebar import render_sidebar

# Import views (renamed from pages/ to views/ to prevent Streamlit multipage auto-detection)
from views.login import render_login
from views.student_dashboard import render_student_dashboard
from views.ai_assistant import render_ai_assistant
from views.notices import render_notices
from views.timetable import render_timetable
from views.chat_history import render_chat_history
from views.profile import render_profile
from views.admin_dashboard import render_admin_dashboard
from views.admin_documents import render_admin_documents
from views.admin_notices import render_admin_notices
from views.admin_faqs import render_admin_faqs
from views.admin_timetable import render_admin_timetable
from views.admin_queries import render_admin_queries
from views.admin_evaluation import render_admin_evaluation

st.set_page_config(page_title="College Helpdesk", layout="wide")

def main():
    init_session()
    apply_styles()
    
    # Check if query params specify a page
    try:
        query_page = st.query_params.get("page")
        if query_page:
            valid_pages = [
                "login", "student_dashboard", "ai_assistant", "notices",
                "timetable", "chat_history", "profile", "admin_dashboard",
                "admin_documents", "admin_notices", "admin_faqs",
                "admin_timetable", "admin_queries", "admin_evaluation"
            ]
            if query_page in valid_pages:
                if is_authenticated():
                    st.session_state.current_page = query_page
                elif query_page == "login":
                    st.session_state.current_page = "login"
    except Exception:
        pass

    if st.session_state.current_page != "login":
        render_sidebar()
        
    page = st.session_state.current_page
    
    if page == "login":
        render_login()
    elif page == "student_dashboard":
        render_student_dashboard()
    elif page == "ai_assistant":
        render_ai_assistant()
    elif page == "notices":
        render_notices()
    elif page == "timetable":
        render_timetable()
    elif page == "chat_history":
        render_chat_history()
    elif page == "profile":
        render_profile()
    elif page == "admin_dashboard":
        render_admin_dashboard()
    elif page == "admin_documents":
        render_admin_documents()
    elif page == "admin_notices":
        render_admin_notices()
    elif page == "admin_faqs":
        render_admin_faqs()
    elif page == "admin_timetable":
        render_admin_timetable()
    elif page == "admin_queries":
        render_admin_queries()
    elif page == "admin_evaluation":
        render_admin_evaluation()
    else:
        st.error("Page not found")

if __name__ == "__main__":
    main()
