from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models.user import User
from backend.models.notice import Notice
from backend.models.timetable import Timetable
from backend.models.chat import Feedback, ChatHistory
from backend.api.deps import get_current_user
from backend.schemas.chat import FeedbackCreate
from typing import Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/dashboard")
def get_dashboard(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    total_conversations = db.query(ChatHistory.conversation_id).filter(
        ChatHistory.user_id == current_user.id
    ).distinct().count()
    total_questions = db.query(ChatHistory).filter(
        ChatHistory.user_id == current_user.id,
        ChatHistory.role == "user"
    ).count()
    return {
        "total_conversations": total_conversations,
        "total_questions": total_questions,
        "user": {
            "full_name": current_user.full_name,
            "department": current_user.department,
            "semester": current_user.semester
        }
    }

@router.get("/timetable")
def get_timetable(
    department: Optional[str] = None,
    semester: Optional[int] = None,
    day: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Timetable)
    if department:
        query = query.filter(Timetable.department == department)
    if semester is not None:
        query = query.filter(Timetable.semester == semester)
    if day:
        query = query.filter(Timetable.day_of_week == day)
    results = query.order_by(Timetable.start_time).all()
    return [
        {
            "id": t.id,
            "department": t.department,
            "semester": t.semester,
            "day_of_week": t.day_of_week,
            "subject": t.subject,
            "start_time": t.start_time,
            "end_time": t.end_time,
            "faculty_name": t.faculty_name,
            "room_number": t.room_number
        }
        for t in results
    ]

@router.get("/notices")
def get_notices(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    notices = db.query(Notice).filter(
        (Notice.expires_at.is_(None)) | (Notice.expires_at >= datetime.utcnow())
    ).order_by(Notice.created_at.desc()).limit(20).all()
    return [
        {
            "id": n.id,
            "title": n.title,
            "content": n.content,
            "category": n.category or "General",
            "priority": n.priority or "Medium",
            "date": n.created_at.strftime("%Y-%m-%d %H:%M") if n.created_at else "Unknown"
        }
        for n in notices
    ]

@router.post("/feedback")
def submit_feedback(feedback: FeedbackCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    chat_message = db.query(ChatHistory).filter(
        ChatHistory.id == feedback.chat_id,
        ChatHistory.user_id == current_user.id,
        ChatHistory.role == "assistant",
    ).first()
    if chat_message is None:
        raise HTTPException(status_code=404, detail="Assistant response not found")
    db_feedback = Feedback(
        user_id=current_user.id,
        chat_id=feedback.chat_id,
        rating=feedback.rating,
        comments=feedback.comments
    )
    db.add(db_feedback)
    db.commit()
    return {"message": "Feedback submitted successfully"}
