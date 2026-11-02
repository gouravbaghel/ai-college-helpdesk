import streamlit as st
from utils.api import get, post, delete
from components.header import render_header

def render_admin_documents():
    render_header("Document Management", "Upload and manage college documents for the AI knowledge base")
    
    # Upload section
    st.subheader("Upload New Document")
    
    with st.form("upload_form", clear_on_submit=True):
        uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])
        category = st.selectbox("Document Category", [
            "General", "Examination", "Attendance", "Academic Calendar",
            "Syllabus", "Fees", "Scholarship", "Hostel", "Notices",
            "Department", "Faculty", "Administration"
        ])
        submit = st.form_submit_button("Upload & Process", use_container_width=True)
        
        if submit and uploaded_file:
            with st.spinner("Uploading and processing document... This may take a moment."):
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                data = {"category": category}
                
                result = post("/admin/documents/upload", data=data, files=files)
                if result:
                    st.success(f"{result.get('message', 'Upload completed')}. {result.get('chunks', 0)} chunks processed.")
                    st.rerun()
        elif submit:
            st.warning("Please select a file to upload.")
    
    st.markdown("---")
    
    # Document list
    st.subheader("Uploaded Documents")
    docs = get("/admin/documents")
    
    if docs:
        for doc in docs:
            col1, col2, col3, col4, col5 = st.columns([3, 2, 1, 2, 1])
            with col1:
                st.markdown(f"**{doc.get('filename', 'Unknown')}**")
            with col2:
                st.markdown(f"{doc.get('category', 'General')}")
            with col3:
                st.markdown(f"{doc.get('chunk_count', 0)} chunks")
            with col4:
                st.markdown(f"{doc.get('upload_date', 'Unknown')}")
            with col5:
                if st.button("Delete", key=f"del_doc_{doc.get('id')}"):
                    result = delete(f"/admin/documents/{doc.get('id')}")
                    if result:
                        st.success("Document deleted.")
                        st.rerun()
            st.markdown("---")
    else:
        st.info("No documents uploaded yet. Upload a PDF above to get started.")
