from sqlalchemy.orm import Session
from sqlalchemy import func
from backend.models.chat import ChatHistory
import uuid

def save_chat_message(db: Session, user_id: int, conversation_id: str, role: str, content: str, sources: list = None):
    if not conversation_id:
        conversation_id = str(uuid.uuid4())
    msg = ChatHistory(
        user_id=user_id,
        conversation_id=conversation_id,
        role=role,
        content=content,
        sources=sources
    )
    db.add(msg)
    db.commit()
    db.refresh(msg)
    return msg

def get_conversations(db: Session, user_id: int):
    """Get list of conversations for a user"""
    from sqlalchemy import distinct
    conv_ids = db.query(ChatHistory.conversation_id).filter(
        ChatHistory.user_id == user_id
    ).distinct().all()
    
    conversations = []
    for (conv_id,) in conv_ids:
        first_msg = db.query(ChatHistory).filter(
            ChatHistory.conversation_id == conv_id,
            ChatHistory.role == "user"
        ).order_by(ChatHistory.timestamp.asc()).first()
        last_msg = db.query(ChatHistory).filter(
            ChatHistory.conversation_id == conv_id
        ).order_by(ChatHistory.timestamp.desc()).first()
        
        title = first_msg.content[:50] + "..." if first_msg and len(first_msg.content) > 50 else (first_msg.content if first_msg else "Conversation")
        
        conversations.append({
            "id": conv_id,
            "title": title,
            "last_message": last_msg.content[:100] if last_msg else "",
            "date": last_msg.timestamp.strftime("%Y-%m-%d %H:%M") if last_msg and last_msg.timestamp else "Unknown"
        })
    
    return sorted(conversations, key=lambda x: x["date"], reverse=True)

def get_conversation_messages(db: Session, user_id: int, conversation_id: str):
    """Get all messages in a conversation"""
    messages = db.query(ChatHistory).filter(
        ChatHistory.conversation_id == conversation_id,
        ChatHistory.user_id == user_id
    ).order_by(ChatHistory.timestamp.asc()).all()
    
    return [
        {
            "id": m.id,
            "role": m.role,
            "content": m.content,
            "sources": m.sources,
            "timestamp": m.timestamp.strftime("%Y-%m-%d %H:%M") if m.timestamp else "Unknown"
        }
        for m in messages
    ]

def get_chat_history(db: Session, user_id: int):
    return db.query(ChatHistory).filter(ChatHistory.user_id == user_id).order_by(ChatHistory.timestamp.asc()).all()
