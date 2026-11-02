import streamlit as st
from utils.api import get
from components.header import render_header
import pandas as pd

def render_admin_queries():
    render_header("User Queries", "View all student questions and AI responses")
    
    queries = get("/admin/queries")
    
    if queries:
        # Filter
        filter_option = st.radio("Filter", ["All", "Answered", "Unanswered"], horizontal=True)
        
        filtered = queries
        if filter_option == "Answered":
            filtered = [q for q in queries if q.get("has_response")]
        elif filter_option == "Unanswered":
            filtered = [q for q in queries if not q.get("has_response")]
        
        st.markdown(f"**Showing {len(filtered)} queries**")
        st.markdown("---")
        
        for q in filtered:
            status_label = "[Answered]" if q.get("has_response") else "[Pending]"
            with st.expander(f"{status_label} {q.get('question', '')[:80]}... | {q.get('username', 'Unknown')} | {q.get('timestamp', '')}"):
                st.markdown(f"**Question:** {q.get('question', '')}")
                st.markdown(f"**Answer:** {q.get('answer', 'No response')}")
                st.markdown(f"**User:** {q.get('username', 'Unknown')}")
                st.markdown(f"**Time:** {q.get('timestamp', 'Unknown')}")
    else:
        st.info("No user queries found yet.")
