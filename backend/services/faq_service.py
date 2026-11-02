from sqlalchemy.orm import Session
from backend.models.faq import FAQ
from backend.schemas.faq import FAQCreate

def create_faq(db: Session, faq: FAQCreate, user_id: int):
    db_faq = FAQ(**faq.model_dump(), created_by=user_id)
    db.add(db_faq)
    db.commit()
    db.refresh(db_faq)
    return {"id": db_faq.id, "message": "FAQ created"}

def get_faqs(db: Session):
    faqs = db.query(FAQ).all()
    return [
        {
            "id": f.id,
            "question": f.question,
            "answer": f.answer,
            "category": f.category or "General"
        }
        for f in faqs
    ]

def update_faq(db: Session, faq_id: int, faq_data: FAQCreate):
    faq = db.query(FAQ).filter(FAQ.id == faq_id).first()
    if faq:
        for key, value in faq_data.model_dump().items():
            setattr(faq, key, value)
        db.commit()
        return {"message": "FAQ updated"}
    return {"message": "FAQ not found"}

def delete_faq(db: Session, faq_id: int):
    faq = db.query(FAQ).filter(FAQ.id == faq_id).first()
    if faq:
        db.delete(faq)
        db.commit()
        return {"message": "FAQ deleted"}
    return {"message": "FAQ not found"}
