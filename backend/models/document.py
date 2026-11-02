from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from backend.database import Base
import datetime

class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True, nullable=False)
    file_path = Column(String, nullable=False)
    category = Column(String, nullable=True, default="General")
    chunk_count = Column(Integer, default=0)
    uploaded_by = Column(Integer, ForeignKey("users.id"))
    upload_date = Column(DateTime, default=datetime.datetime.utcnow)
