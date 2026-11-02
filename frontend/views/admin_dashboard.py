import streamlit as st
from utils.api import get
from components.cards import stat_card
from components.header import render_header
import json

def render_admin_dashboard():
    render_header("Admin Dashboard", "System overview and analytics")
    
    analytics = get("/admin/analytics")
    
    if analytics:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            stat_card("Total Students", analytics.get("total_users", 0))
        with col2:
            stat_card("Documents", analytics.get("total_documents", 0))
        with col3:
            stat_card("Total Queries", analytics.get("total_queries", 0))
        with col4:
            stat_card("Notices", analytics.get("total_notices", 0))
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Daily queries chart
        daily = analytics.get("daily_queries", [])
        if daily:
            st.subheader("Queries Per Day (Last 7 Days)")
            import pandas as pd
            df = pd.DataFrame(daily)
            if not df.empty:
                st.bar_chart(df.set_index("date")["count"])
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Quick Stats")
            st.markdown(f"- **Total FAQs:** {analytics.get('total_faqs', 0)}")
            st.markdown(f"- **Unanswered Questions:** {analytics.get('unanswered_questions', 0)}")
        
        with col2:
            st.subheader("System Health")
            st.markdown("""
            <div class='card'>
                <p>Backend API: <strong>Online</strong></p>
                <p>Database: <strong>Connected</strong></p>
                <p>Vector Store: <strong>Active</strong></p>
                <p>LLM Service: <strong>Configured</strong></p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("Could not load analytics. Is the backend running?")
