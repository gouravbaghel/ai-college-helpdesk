import streamlit as st
from utils.api import get
from components.header import render_header

def render_profile():
    render_header("Student Profile", "Account details and enrolled academic information")
    
    user = get("/auth/me")
    if user:
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown(f"""
            <div class="card">
                <div style="display: flex; align-items: center; gap: 16px; margin-bottom: 1.25rem;">
                    <div style="width: 52px; height: 52px; border-radius: 50%; background: linear-gradient(135deg, var(--primary), var(--secondary)); display: flex; align-items: center; justify-content: center; color: white; font-weight: 700; font-size: 1.25rem;">
                        {user.get('full_name', 'S')[0].upper()}
                    </div>
                    <div>
                        <h3 style="margin: 0; color: var(--primary);">{user.get('full_name', 'Student')}</h3>
                        <p style="margin: 0; color: var(--text-muted); font-size: 0.85rem;">@{user.get('username')}</p>
                    </div>
                </div>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; border-top: 1px solid var(--border-light); padding-top: 1rem;">
                    <div>
                        <span style="font-size: 0.8rem; color: var(--text-muted); text-transform: uppercase;">Email Address</span>
                        <p style="margin: 2px 0 0 0; font-weight: 500;">{user.get('email', 'N/A')}</p>
                    </div>
                    <div>
                        <span style="font-size: 0.8rem; color: var(--text-muted); text-transform: uppercase;">Enrollment Number</span>
                        <p style="margin: 2px 0 0 0; font-weight: 500;">{user.get('enrollment_number', 'Not registered')}</p>
                    </div>
                    <div>
                        <span style="font-size: 0.8rem; color: var(--text-muted); text-transform: uppercase;">Academic Department</span>
                        <p style="margin: 2px 0 0 0; font-weight: 500;">{user.get('department', 'General')}</p>
                    </div>
                    <div>
                        <span style="font-size: 0.8rem; color: var(--text-muted); text-transform: uppercase;">Current Semester</span>
                        <p style="margin: 2px 0 0 0; font-weight: 500;">Semester {user.get('semester', '1')}</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.markdown("""
            <div class="card">
                <h4 style="margin-top: 0; color: var(--primary);">Account Status</h4>
                <p style="margin: 0 0 8px 0; font-size: 0.9rem; color: var(--text-secondary);">Active enrolled student profile.</p>
                <span class="category-badge" style="background: rgba(13, 148, 136, 0.1); color: var(--secondary);">Verified Student</span>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("Unable to retrieve student profile. Please verify connection to the backend server.")
