import streamlit as st
from utils.api import get
from utils.session import set_page
from components.cards import stat_card, notice_card

def render_student_dashboard():
    dashboard_data = get("/student/dashboard")
    
    user_info = dashboard_data.get("user", {}) if dashboard_data else {}
    name = user_info.get("full_name") or (st.session_state.user_info.get("username", "Student") if st.session_state.user_info else "Student")
    dept = user_info.get("department") or "General"
    sem = user_info.get("semester") or 1
    
    st.markdown(f"<h2 class='main-header'>Student Dashboard</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='color: var(--text-secondary); margin-top: -6px; font-size: 1.05rem;'>Welcome back, <strong>{name}</strong></p>", unsafe_allow_html=True)
    st.markdown("<div class='header-divider'></div>", unsafe_allow_html=True)
    
    # Summary Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        stat_card("Department", dept)
    with col2:
        stat_card("Semester", f"Sem {sem}")
    with col3:
        stat_card("Queries Asked", dashboard_data.get("total_questions", 0) if dashboard_data else 0)
    with col4:
        stat_card("Conversations", dashboard_data.get("total_conversations", 0) if dashboard_data else 0)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Quick Navigation Actions
    st.subheader("Quick Actions")
    act_col1, act_col2, act_col3, act_col4 = st.columns(4)
    with act_col1:
        if st.button("Ask AI Assistant", use_container_width=True, type="primary"):
            set_page("ai_assistant")
    with act_col2:
        if st.button("View Timetable", use_container_width=True):
            set_page("timetable")
    with act_col3:
        if st.button("Browse Notices", use_container_width=True):
            set_page("notices")
    with act_col4:
        if st.button("Chat History", use_container_width=True):
            set_page("chat_history")
            
    st.markdown("<div class='header-divider' style='margin: 1.5rem 0;'></div>", unsafe_allow_html=True)
    
    # Recent Notices Section
    st.subheader("Recent Announcements")
    notices = get("/student/notices")
    if notices:
        for n in notices[:3]:
            notice_card(
                n.get("title", "Notice"),
                n.get("content", ""),
                n.get("date", "Recent"),
                n.get("category", "General")
            )
        if len(notices) > 3:
            if st.button("View All Notices", use_container_width=False):
                set_page("notices")
    else:
        notice_card("Welcome to College Helpdesk", "Access your timetable, examination policies, syllabus, and college regulations via the AI Assistant.", "Today", "General")
