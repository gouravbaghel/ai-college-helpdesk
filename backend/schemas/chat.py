from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class ChatRequest(BaseModel):
    question: str
    conversation_id: Optional[str] = None

class SourceInfo(BaseModel):
    document_name: str = "Unknown"
    page_number: int = 0
    category: str = "General"

class ChatResponse(BaseModel):
    answer: str
    sources: List[Dict[str, Any]] = []
    conversation_id: str

class ChatMessageResponse(BaseModel):
    id: int
    role: str
    content: str
    sources: Optional[List[Dict[str, Any]]] = None
    timestamp: datetime

    class Config:
        from_attributes = True

class ConversationResponse(BaseModel):
    conversation_id: str
    title: str
    last_message: str
    timestamp: datetime

class FeedbackCreate(BaseModel):
    chat_id: int = Field(gt=0)
    rating: int = Field(ge=1, le=5)
    comments: Optional[str] = None
