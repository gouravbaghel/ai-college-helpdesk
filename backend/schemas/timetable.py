from pydantic import BaseModel
from typing import Optional

class TimetableCreate(BaseModel):
    department: str
    semester: int
    day_of_week: str
    subject: str
    start_time: str
    end_time: str
    faculty_name: str
    room_number: str

class TimetableResponse(TimetableCreate):
    id: int

    class Config:
        from_attributes = True
