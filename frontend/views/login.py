import streamlit as st
from utils.api import post
from utils.session import login

def render_login():
    st.markdown("<h1 style='text-align: center; color: var(--primary);'>College Helpdesk</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #666;'>Welcome to the AI-Powered College Helpdesk & Student Assistant</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        tab1, tab2 = st.tabs(["Login", "Register"])
        
        with tab1:
            with st.form("login_form"):
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                submit = st.form_submit_button("Login", use_container_width=True)
                
                if submit:
                    if username and password:
                        response = post("/auth/login", data={"username": username, "password": password})
                        if response and "access_token" in response:
                            st.success("Login successful!")
                            role = response.get("role", "student")
                            login(response["access_token"], role, {"username": username})
                    else:
                        st.warning("Please enter username and password")
                        
        with tab2:
            with st.form("register_form"):
                reg_username = st.text_input("Username")
                reg_password = st.text_input("Password", type="password")
                full_name = st.text_input("Full Name")
                email = st.text_input("Email")
                department = st.text_input("Department (Optional)")
                semester = st.number_input("Semester (Optional)", min_value=1, max_value=10, value=1)
                enrollment_number = st.text_input("Enrollment Number (Optional)")
                
                reg_submit = st.form_submit_button("Register", use_container_width=True)
                
                if reg_submit:
                    if reg_username and reg_password and full_name and email:
                        data = {
                            "username": reg_username,
                            "password": reg_password,
                            "full_name": full_name,
                            "email": email,
                            "department": department if department else None,
                            "semester": semester,
                            "enrollment_number": enrollment_number if enrollment_number else None
                        }
                        response = post("/auth/register", data=data)
                        if response:
                            st.success("Registration successful! Please login.")
                    else:
                        st.warning("Please fill all required fields")
