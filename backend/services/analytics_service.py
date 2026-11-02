from sqlalchemy.orm import Session
from sqlalchemy import func
from backend.models.user import User
from backend.models.document import Document
from backend.models.chat import ChatHistory, Feedback
from backend.models.notice import Notice
from backend.models.faq import FAQ
from datetime import datetime, timedelta

def get_dashboard_analytics(db: Session):
    total_users = db.query(User).filter(User.role == "student").count()
    total_docs = db.query(Document).count()
    total_queries = db.query(ChatHistory).filter(ChatHistory.role == "user").count()
    total_notices = db.query(Notice).count()
    total_faqs = db.query(FAQ).count()
    
    # Queries per day (last 7 days)
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    daily_queries = []
    for i in range(7):
        day = datetime.utcnow() - timedelta(days=6-i)
        day_start = day.replace(hour=0, minute=0, second=0, microsecond=0)
        day_end = day.replace(hour=23, minute=59, second=59, microsecond=999999)
        count = db.query(ChatHistory).filter(
            ChatHistory.role == "user",
            ChatHistory.timestamp >= day_start,
            ChatHistory.timestamp <= day_end
        ).count()
        daily_queries.append({"date": day_start.strftime("%Y-%m-%d"), "count": count})
    
    # Unanswered count (queries without response)
    unanswered = 0  # Simplified - all queries get responses
    
    return {
        "total_users": total_users,
        "total_documents": total_docs,
        "total_queries": total_queries,
        "total_notices": total_notices,
        "total_faqs": total_faqs,
        "unanswered_questions": unanswered,
        "daily_queries": daily_queries
    }
