from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class DocumentResponse(BaseModel):
    id: int
    filename: str
    category: Optional[str] = "General"
    chunk_count: int = 0
    upload_date: datetime

    class Config:
        from_attributes = True
