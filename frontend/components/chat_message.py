import streamlit as st

def render_message(role, content, sources=None):
    if role == "user":
        st.markdown(f"""
        <div style="display: flex; justify-content: flex-end;">
            <div class="chat-msg chat-user">
                {content}
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        sources_html = ""
        if sources:
            sources_html = "<div style='margin-top: 10px;'>"
            for src in sources:
                sources_html += f"<span class='source-doc'>Source: {src.get('document_name', 'Unknown')} | Page: {src.get('page_number', '?')} | Category: {src.get('category', 'General')}</span>"
            sources_html += "</div>"
            
        st.markdown(f"""
        <div style="display: flex; justify-content: flex-start;">
            <div class="chat-msg chat-assistant">
                <div>{content}</div>
                {sources_html}
            </div>
        </div>
        """, unsafe_allow_html=True)
