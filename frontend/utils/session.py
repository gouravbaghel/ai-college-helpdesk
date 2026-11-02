import streamlit as st

def init_session():
    defaults = {
        "token": None,
        "role": None,
        "user_info": None,
        "current_page": "login",
        "conversation_id": None
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def set_page(page_name):
    st.session_state.current_page = page_name
    st.query_params["page"] = page_name
    st.rerun()

def login(token, role, user_info=None):
    st.session_state.token = token
    st.session_state.role = role
    st.session_state.user_info = user_info
    if role == "admin":
        set_page("admin_dashboard")
    else:
        set_page("student_dashboard")

def logout():
    st.session_state.token = None
    st.session_state.role = None
    st.session_state.user_info = None
    st.session_state.conversation_id = None
    try:
        if "page" in st.query_params:
            del st.query_params["page"]
    except Exception:
        pass
    st.session_state.current_page = "login"
    st.rerun()

def is_authenticated():
    return st.session_state.token is not None
