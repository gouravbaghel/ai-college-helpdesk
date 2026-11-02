from sqlalchemy.orm import Session
from backend.models.timetable import Timetable
from backend.schemas.timetable import TimetableCreate

def create_timetable(db: Session, timetable: TimetableCreate):
    db_tt = Timetable(**timetable.model_dump())
    db.add(db_tt)
    db.commit()
    db.refresh(db_tt)
    return {"id": db_tt.id, "message": "Timetable entry created"}

def get_timetables(db: Session, department: str = None):
    query = db.query(Timetable)
    if department:
        query = query.filter(Timetable.department == department)
    results = query.order_by(Timetable.day_of_week, Timetable.start_time).all()
    return [
        {
            "id": t.id,
            "department": t.department,
            "semester": t.semester,
            "day_of_week": t.day_of_week,
            "subject": t.subject,
            "start_time": t.start_time,
            "end_time": t.end_time,
            "faculty_name": t.faculty_name,
            "room_number": t.room_number
        }
        for t in results
    ]

def delete_timetable(db: Session, tt_id: int):
    tt = db.query(Timetable).filter(Timetable.id == tt_id).first()
    if tt:
        db.delete(tt)
        db.commit()
        return {"message": "Timetable entry deleted"}
    return {"message": "Timetable entry not found"}
