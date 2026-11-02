import streamlit as st
from utils.api import post, get
from components.chat_message import render_message
from utils.session import set_page

def render_ai_assistant():
    st.markdown("<h2 class='main-header'>AI Assistant</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 4])
    
    with col1:
        st.markdown("### Conversations")
        if st.button("New Chat", use_container_width=True):
            st.session_state.conversation_id = None
            if "messages" in st.session_state:
                st.session_state.messages = []
            st.rerun()
            
        history = get("/chat/history")
        if history:
            for chat in history:
                title = chat.get('title', 'Chat ' + str(chat.get('id', ''))[:8])
                if st.button(title, key=f"hist_{chat.get('id')}", use_container_width=True):
                    st.session_state.conversation_id = chat.get('id')
                    st.session_state.messages = []
                    # Fetch details
                    details = get(f"/chat/history/{chat.get('id')}")
                    if details and isinstance(details, list):
                        st.session_state.messages = details
                    st.rerun()

    with col2:
        if "messages" not in st.session_state:
            st.session_state.messages = []
            
        # Display chat messages
        chat_container = st.container(height=500)
        with chat_container:
            for msg in st.session_state.messages:
                render_message(msg["role"], msg["content"], msg.get("sources"))
                
        # Input area
        with st.form("chat_form", clear_on_submit=True):
            col_in1, col_in2 = st.columns([5, 1])
            with col_in1:
                question = st.text_input("Ask a question about college...", label_visibility="collapsed")
            with col_in2:
                submit = st.form_submit_button("Send", use_container_width=True)
                
            if submit and question:
                st.session_state.messages.append({"role": "user", "content": question})
                
                data = {"question": question}
                if st.session_state.conversation_id:
                    data["conversation_id"] = st.session_state.conversation_id
                    
                with st.spinner("AI is thinking..."):
                    response = post("/chat/ask", data=data)
                    
                if response:
                    answer = response.get("answer", "No answer provided.")
                    sources = response.get("sources", [])
                    conv_id = response.get("conversation_id")
                    
                    if conv_id:
                        st.session_state.conversation_id = conv_id
                        
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer,
                        "sources": sources
                    })
                st.rerun()
