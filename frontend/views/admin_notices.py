import streamlit as st
from utils.api import get, post, put, delete
from components.header import render_header

def render_admin_notices():
    render_header("Notice Management", "Create, edit, and manage college notices")
    
    # Create notice
    st.subheader("Create New Notice")
    with st.form("create_notice_form", clear_on_submit=True):
        title = st.text_input("Title")
        content = st.text_area("Content", height=100)
        col1, col2 = st.columns(2)
        with col1:
            category = st.selectbox("Category", [
                "General", "Examination", "Academic", "Placement",
                "Fees", "Holiday", "Events", "Administration"
            ])
        with col2:
            priority = st.selectbox("Priority", ["Low", "Medium", "High", "Urgent"])
        
        submit = st.form_submit_button("Create Notice", use_container_width=True)
        if submit and title and content:
            result = post("/admin/notices", data={
                "title": title,
                "content": content,
                "category": category,
                "priority": priority
            })
            if result:
                st.success("Notice created successfully!")
                st.rerun()
    
    st.markdown("---")
    
    # List notices
    st.subheader("Existing Notices")
    notices = get("/admin/notices")
    
    if notices:
        for notice in notices:
            priority = notice.get("priority", "Medium")
            priority_labels = {"Low": "[Low]", "Medium": "[Medium]", "High": "[High]", "Urgent": "[Urgent]"}
            priority_label = priority_labels.get(priority, "[Medium]")
            
            with st.expander(f"{priority_label} {notice.get('title', 'Untitled')} | {notice.get('category', 'General')} | {notice.get('created_at', '')}"):
                st.write(notice.get("content", ""))
                col1, col2 = st.columns(2)
                with col2:
                    if st.button("Delete", key=f"del_notice_{notice.get('id')}"):
                        result = delete(f"/admin/notices/{notice.get('id')}")
                        if result:
                            st.success("Notice deleted.")
                            st.rerun()
    else:
        st.info("No notices yet.")
