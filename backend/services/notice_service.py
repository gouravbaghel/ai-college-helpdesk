from sqlalchemy.orm import Session
from backend.models.notice import Notice
from backend.schemas.notice import NoticeCreate

def create_notice(db: Session, notice: NoticeCreate, user_id: int):
    db_notice = Notice(**notice.model_dump(), posted_by=user_id)
    db.add(db_notice)
    db.commit()
    db.refresh(db_notice)
    return {"id": db_notice.id, "message": "Notice created"}

def get_notices(db: Session, skip: int = 0, limit: int = 100):
    notices = db.query(Notice).order_by(Notice.created_at.desc()).offset(skip).limit(limit).all()
    return [
        {
            "id": n.id,
            "title": n.title,
            "content": n.content,
            "category": n.category or "General",
            "priority": n.priority or "Medium",
            "created_at": n.created_at.strftime("%Y-%m-%d %H:%M") if n.created_at else "Unknown"
        }
        for n in notices
    ]

def update_notice(db: Session, notice_id: int, notice_data: NoticeCreate):
    notice = db.query(Notice).filter(Notice.id == notice_id).first()
    if notice:
        for key, value in notice_data.model_dump().items():
            setattr(notice, key, value)
        db.commit()
        return {"message": "Notice updated"}
    return {"message": "Notice not found"}

def delete_notice(db: Session, notice_id: int):
    notice = db.query(Notice).filter(Notice.id == notice_id).first()
    if notice:
        db.delete(notice)
        db.commit()
        return {"message": "Notice deleted"}
    return {"message": "Notice not found"}
