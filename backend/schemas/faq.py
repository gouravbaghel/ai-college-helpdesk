from pydantic import BaseModel
from typing import Optional

class FAQCreate(BaseModel):
    question: str
    answer: str
    category: Optional[str] = "General"

class FAQResponse(FAQCreate):
    id: int

    class Config:
        from_attributes = True
