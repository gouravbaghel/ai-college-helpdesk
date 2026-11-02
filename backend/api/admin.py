from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models.user import User
from backend.models.chat import ChatHistory
from backend.api.deps import get_current_admin
from backend.services.document_service import process_and_store_document, get_all_documents, delete_document
from backend.services.notice_service import create_notice, get_notices, update_notice, delete_notice
from backend.services.faq_service import create_faq, get_faqs, update_faq, delete_faq
from backend.services.timetable_service import create_timetable, get_timetables, delete_timetable
from backend.services.analytics_service import get_dashboard_analytics
from backend.schemas.notice import NoticeCreate
from backend.schemas.faq import FAQCreate
from backend.schemas.timetable import TimetableCreate
import json
import os
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/documents/upload")
async def upload_document(
    file: UploadFile = File(...),
    category: str = Form(default="General"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    result = await process_and_store_document(file, category, db, current_user.id)
    return result

@router.get("/documents")
def get_documents(db: Session = Depends(get_db), current_user: User = Depends(get_current_admin)):
    docs = get_all_documents(db)
    return [
        {
            "id": d.id,
            "filename": d.filename,
            "category": d.category or "General",
            "chunk_count": d.chunk_count or 0,
            "upload_date": d.upload_date.strftime("%Y-%m-%d %H:%M") if d.upload_date else "Unknown"
        }
        for d in docs
    ]

@router.delete("/documents/{doc_id}")
def delete_doc(doc_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_admin)):
    return delete_document(db, doc_id)

@router.post("/notices")
def add_notice(notice: NoticeCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_admin)):
    return create_notice(db, notice, current_user.id)

@router.get("/notices")
def list_notices(db: Session = Depends(get_db), current_user: User = Depends(get_current_admin)):
    return get_notices(db)

@router.put("/notices/{notice_id}")
def edit_notice(notice_id: int, notice: NoticeCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_admin)):
    return update_notice(db, notice_id, notice)

@router.delete("/notices/{notice_id}")
def remove_notice(notice_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_admin)):
    return delete_notice(db, notice_id)

@router.post("/faqs")
def add_faq(faq: FAQCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_admin)):
    return create_faq(db, faq, current_user.id)

@router.get("/faqs")
def list_faqs(db: Session = Depends(get_db), current_user: User = Depends(get_current_admin)):
    return get_faqs(db)

@router.put("/faqs/{faq_id}")
def edit_faq(faq_id: int, faq: FAQCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_admin)):
    return update_faq(db, faq_id, faq)

@router.delete("/faqs/{faq_id}")
def remove_faq(faq_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_admin)):
    return delete_faq(db, faq_id)

@router.post("/timetable")
def add_timetable(timetable: TimetableCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_admin)):
    return create_timetable(db, timetable)

@router.get("/timetable")
def list_timetable(db: Session = Depends(get_db), current_user: User = Depends(get_current_admin)):
    return get_timetables(db)

@router.delete("/timetable/{tt_id}")
def remove_timetable(tt_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_admin)):
    return delete_timetable(db, tt_id)

@router.get("/analytics")
def get_analytics(db: Session = Depends(get_db), current_user: User = Depends(get_current_admin)):
    return get_dashboard_analytics(db)

@router.get("/queries")
def get_user_queries(db: Session = Depends(get_db), current_user: User = Depends(get_current_admin)):
    queries = db.query(ChatHistory).filter(ChatHistory.role == "user").order_by(ChatHistory.timestamp.desc()).limit(100).all()
    result = []
    for q in queries:
        # Find the assistant response
        response = db.query(ChatHistory).filter(
            ChatHistory.conversation_id == q.conversation_id,
            ChatHistory.user_id == q.user_id,
            ChatHistory.role == "assistant",
            ChatHistory.timestamp > q.timestamp
        ).order_by(ChatHistory.timestamp.asc()).first()
        user = db.query(User).filter(User.id == q.user_id).first()
        result.append({
            "id": q.id,
            "question": q.content,
            "answer": response.content if response else "No response",
            "username": user.username if user else "Unknown",
            "timestamp": q.timestamp.strftime("%Y-%m-%d %H:%M") if q.timestamp else "Unknown",
            "has_response": response is not None
        })
    return result

@router.get("/evaluation")
def get_evaluation(current_user: User = Depends(get_current_admin)):
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    eval_file = os.path.join(project_root, "evaluation_results.json")
    if os.path.exists(eval_file):
        with open(eval_file, "r") as f:
            return json.load(f)
    return {
        "metrics": {
            "retrieval_accuracy": 0,
            "answer_relevance": 0,
            "citation_accuracy": 0,
            "avg_response_time": 0,
            "unanswered_questions": 0
        },
        "test_results": [],
        "message": "No evaluation has been run yet. Run tests/test_rag_evaluation.py to generate results."
    }
