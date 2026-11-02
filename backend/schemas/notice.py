from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class NoticeCreate(BaseModel):
    title: str
    content: str
    category: Optional[str] = "General"
    priority: Optional[str] = "Medium"
    expires_at: Optional[datetime] = None

class NoticeResponse(BaseModel):
    id: int
    title: str
    content: str
    category: str = "General"
    priority: str = "Medium"
    created_at: datetime
    expires_at: Optional[datetime] = None

    class Config:
        from_attributes = True
