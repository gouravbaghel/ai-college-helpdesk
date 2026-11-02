from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from backend.database import get_db
from backend.models.user import User
from backend.models.chat import ChatHistory
from backend.api.deps import get_current_user
from backend.schemas.chat import ChatRequest, ChatResponse
from backend.services.chat_service import save_chat_message, get_conversations, get_conversation_messages
from backend.agents.college_agent import generate_response
import uuid
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/ask", response_model=ChatResponse)
def ask_question(request: ChatRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    conversation_id = request.conversation_id or str(uuid.uuid4())
    user_question = request.question
    
    # Save user message
    save_chat_message(db, current_user.id, conversation_id, "user", user_question)
    
    try:
        # Generate response via Agent
        response_data = generate_response(user_question, current_user.id, db)
        bot_message = response_data.get("answer", "I'm sorry, I couldn't process your question.")
        sources = response_data.get("sources", [])
    except Exception as e:
        logger.error(f"Error generating response: {e}")
        bot_message = "I'm sorry, I encountered an error while processing your question. Please try again."
        sources = []
    
    # Save bot message
    save_chat_message(db, current_user.id, conversation_id, "assistant", bot_message, sources)
    
    return ChatResponse(
        answer=bot_message,
        sources=sources,
        conversation_id=conversation_id
    )

@router.get("/history")
def get_history(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_conversations(db, current_user.id)

@router.get("/history/{conversation_id}")
def get_conversation(conversation_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_conversation_messages(db, current_user.id, conversation_id)
