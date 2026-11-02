from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from backend.database import Base
import datetime

class FAQ(Base):
    __tablename__ = "faqs"
    id = Column(Integer, primary_key=True, index=True)
    question = Column(String, index=True, nullable=False)
    answer = Column(Text, nullable=False)
    category = Column(String, default="General")
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
