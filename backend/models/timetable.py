from sqlalchemy import Column, Integer, String
from backend.database import Base

class Timetable(Base):
    __tablename__ = "timetables"
    id = Column(Integer, primary_key=True, index=True)
    department = Column(String, index=True, nullable=False)
    semester = Column(Integer, nullable=False)
    day_of_week = Column(String, nullable=False)
    subject = Column(String, nullable=False)
    start_time = Column(String, nullable=False)
    end_time = Column(String, nullable=False)
    faculty_name = Column(String, nullable=False)
    room_number = Column(String, nullable=False)
