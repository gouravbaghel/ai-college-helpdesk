import streamlit as st
from utils.api import get
from utils.session import set_page
from components.header import render_header

def render_chat_history():
    render_header("Consultation History", "Review previous inquiries and AI-grounded responses")
    
    history = get("/chat/history")
    if history:
        for chat in history:
            chat_id = chat.get("id")
            title = chat.get("title", "Consultation")
            date_str = chat.get("date", "Recent")
            
            with st.container():
                st.markdown(f"""
                <div class="card" style="margin-bottom: 0.75rem;">
                    <div style="display: flex; justify-content: space-between; align-items: baseline;">
                        <h4 style="margin: 0; color: var(--primary);">{title}</h4>
                        <span style="font-size: 0.8rem; color: var(--text-muted);">{date_str}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                if st.button("Continue Consultation", key=f"view_{chat_id}", use_container_width=False):
                    details = get(f"/chat/history/{chat_id}")
                    if details is not None:
                        st.session_state.conversation_id = chat_id
                        st.session_state.messages = details if isinstance(details, list) else []
                        set_page("ai_assistant")
    else:
        st.info("No previous consultations on record. Start a conversation with the AI Assistant.")
