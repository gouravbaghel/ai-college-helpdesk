import streamlit as st
from utils.api import get, post, put, delete
from components.header import render_header

def render_admin_faqs():
    render_header("FAQ Management", "Manage frequently asked questions")
    
    # Create FAQ
    st.subheader("Add New FAQ")
    with st.form("create_faq_form", clear_on_submit=True):
        question = st.text_input("Question")
        answer = st.text_area("Answer", height=100)
        category = st.selectbox("Category", [
            "General", "Attendance", "Examination", "Fees",
            "Scholarship", "Hostel", "Placement", "Academic",
            "Administration", "Library"
        ])
        
        submit = st.form_submit_button("Add FAQ", use_container_width=True)
        if submit and question and answer:
            result = post("/admin/faqs", data={
                "question": question,
                "answer": answer,
                "category": category
            })
            if result:
                st.success("FAQ added successfully!")
                st.rerun()
    
    st.markdown("---")
    
    # List FAQs
    st.subheader("Existing FAQs")
    faqs = get("/admin/faqs")
    
    if faqs:
        for faq in faqs:
            with st.expander(f"{faq.get('question', 'Untitled')} | {faq.get('category', 'General')}"):
                st.markdown(f"**Answer:** {faq.get('answer', '')}")
                col1, col2 = st.columns(2)
                with col2:
                    if st.button("Delete", key=f"del_faq_{faq.get('id')}"):
                        result = delete(f"/admin/faqs/{faq.get('id')}")
                        if result:
                            st.success("FAQ deleted.")
                            st.rerun()
    else:
        st.info("No FAQs yet.")
