from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from backend.database import Base
import datetime

class Notice(Base):
    __tablename__ = "notices"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    content = Column(Text, nullable=False)
    category = Column(String, default="General")
    priority = Column(String, default="Medium")  # Low, Medium, High, Urgent
    posted_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)
