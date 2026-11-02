"""
Database seeding script for the College Helpdesk system.
Creates demo users, notices, FAQs, and timetable entries.

Usage: python -m backend.seed_data
"""
import sys
import os

# Ensure the project root is in the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.database import SessionLocal, engine, Base
from backend.models.user import User
from backend.models.timetable import Timetable
from backend.models.notice import Notice
from backend.models.faq import FAQ
from backend.services.auth_service import get_password_hash


def seed():
    """Seed the database with demo data."""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    if db.query(User).first():
        print("Database already seeded. Delete college_helpdesk.db to re-seed.")
        db.close()
        return
    
    print("Seeding database...")
    
    # â”€â”€ Admin User â”€â”€
    admin = User(
        username="admin",
        email="admin@rgit.edu.in",
        full_name="Dr. Rajesh Kumar (Admin)",
        hashed_password=get_password_hash("admin123"),
        role="admin",
        department="Administration"
    )
    db.add(admin)
    db.commit()
    db.refresh(admin)
    
    # â”€â”€ Student Users â”€â”€
    students_data = [
        {"username": "student1", "email": "rahul.sharma@rgit.edu.in", "full_name": "Rahul Sharma",
         "department": "Computer Science", "semester": 5, "enrollment": "CS2022001"},
        {"username": "student2", "email": "priya.patel@rgit.edu.in", "full_name": "Priya Patel",
         "department": "Computer Science", "semester": 3, "enrollment": "CS2023015"},
        {"username": "student3", "email": "amit.singh@rgit.edu.in", "full_name": "Amit Singh",
         "department": "Electronics", "semester": 5, "enrollment": "EC2022008"},
    ]
    
    for s in students_data:
        db.add(User(
            username=s["username"],
            email=s["email"],
            full_name=s["full_name"],
            hashed_password=get_password_hash("password123"),
            role="student",
            department=s["department"],
            semester=s["semester"],
            enrollment_number=s["enrollment"]
        ))
    db.commit()
    print("  [OK] Users created (1 admin, 3 students)")
    
    # â”€â”€ Notices â”€â”€
    notices = [
        {"title": "End Semester Examination Schedule - October 2024",
         "content": "The end semester examinations for all departments will commence from October 15, 2024. Students are advised to collect their hall tickets from the examination cell. Ensure minimum 75% attendance to be eligible.",
         "category": "Examination", "priority": "Urgent"},
        {"title": "Diwali Holiday Notice",
         "content": "The college will remain closed from October 28 to November 3 on account of Diwali vacation. Regular classes will resume on November 4, 2024.",
         "category": "Holiday", "priority": "High"},
        {"title": "Campus Placement Drive - TCS",
         "content": "TCS will be conducting a campus placement drive on November 10, 2024. Eligible students (CGPA >= 7.0, no active backlogs) should register through the placement portal by November 5.",
         "category": "Placement", "priority": "High"},
        {"title": "Fee Payment Deadline Extended",
         "content": "The last date for payment of tuition fees for the odd semester has been extended to October 20, 2024. Late fee of Rs. 500 will be applicable after this date.",
         "category": "Fees", "priority": "High"},
        {"title": "Technical Symposium - TechFest 2024",
         "content": "The annual technical symposium TechFest 2024 will be held on November 15-16, 2024. Students interested in participating in coding contests, paper presentations, and workshops should register at the CS department office.",
         "category": "Events", "priority": "Medium"},
        {"title": "Library Timings Update",
         "content": "Effective immediately, the central library timings have been extended. New timings: Monday to Friday 8:00 AM to 9:00 PM, Saturday 9:00 AM to 5:00 PM. The digital library section is available 24/7.",
         "category": "General", "priority": "Low"},
        {"title": "Anti-Ragging Committee Meeting",
         "content": "All class representatives are requested to attend the Anti-Ragging Committee meeting on October 12 at 3:00 PM in the conference hall. Attendance is mandatory.",
         "category": "Administration", "priority": "High"},
        {"title": "Workshop on Machine Learning",
         "content": "A 3-day workshop on Machine Learning and AI will be conducted by Prof. S. Krishnan from IIT Bombay from October 22-24, 2024. Registration is open for all CS and IT students. Limited seats available.",
         "category": "Academic", "priority": "Medium"},
    ]
    
    for n in notices:
        db.add(Notice(
            title=n["title"], content=n["content"],
            category=n["category"], priority=n["priority"],
            posted_by=admin.id
        ))
    db.commit()
    print(f"  [OK] {len(notices)} notices created")
    
    # â”€â”€ FAQs â”€â”€
    faqs = [
        {"question": "What is the minimum attendance required for examinations?",
         "answer": "Students must maintain a minimum of 75% attendance in each subject to be eligible to appear in the end semester examinations. Students with attendance between 65-75% may apply for condonation with a fee of Rs. 1000 per subject.",
         "category": "Attendance"},
        {"question": "How is the CGPA calculated?",
         "answer": "CGPA is calculated as the weighted average of grade points obtained in all courses. Grade points: O=10, A+=9, A=8, B+=7, B=6, C=5, F=0. CGPA = Sum(Credits Ã— Grade Points) / Total Credits.",
         "category": "Examination"},
        {"question": "What is the fee structure for B.Tech?",
         "answer": "Annual tuition fee for B.Tech is Rs. 1,20,000 for general category and Rs. 60,000 for reserved categories. Additional fees: Library fee Rs. 5,000, Lab fee Rs. 10,000, Examination fee Rs. 3,000 per semester.",
         "category": "Fees"},
        {"question": "How do I apply for a scholarship?",
         "answer": "Scholarships are available for merit (CGPA >= 8.5) and need-based categories. Apply through the scholarship portal within 30 days of semester registration. Required documents: income certificate, mark sheets, and application form.",
         "category": "Scholarship"},
        {"question": "What are the hostel timings?",
         "answer": "Hostel gate timings: Entry by 9:00 PM on weekdays, 10:00 PM on weekends. Mess timings: Breakfast 7:30-9:00 AM, Lunch 12:30-2:00 PM, Snacks 4:30-5:30 PM, Dinner 7:30-9:00 PM.",
         "category": "Hostel"},
        {"question": "How can I get my exam re-evaluated?",
         "answer": "Apply for re-evaluation within 15 days of result declaration. Fee: Rs. 500 per subject. Submit the application at the examination cell with payment receipt. Re-evaluation results are declared within 30 days.",
         "category": "Examination"},
        {"question": "What is the college leave policy for students?",
         "answer": "Students can apply for leave through the student portal. Medical leave requires a medical certificate. Prior permission is required for planned absences. More than 3 consecutive days of unauthorized absence will result in a warning letter to parents.",
         "category": "General"},
        {"question": "How do I access the college WiFi?",
         "answer": "Use your student ID as username and your date of birth (DDMMYYYY) as the initial password on the 'RGIT-Student' network. Change your password after first login through the IT helpdesk portal.",
         "category": "General"},
        {"question": "What are the placement eligibility criteria?",
         "answer": "Minimum CGPA of 6.0 (may vary by company), no active backlogs at the time of placement, minimum 75% attendance. Students must register on the placement portal and attend all pre-placement training sessions.",
         "category": "Placement"},
        {"question": "How do I apply for a bonafide certificate?",
         "answer": "Apply online through the student portal under 'Certificate Requests'. Processing time is 3-5 working days. Collect from the administrative office with your student ID card. Fee: Rs. 100 per certificate.",
         "category": "Administration"},
        {"question": "What is the grading system?",
         "answer": "The college follows a 10-point grading system: O (Outstanding) = 90-100% = 10 points, A+ (Excellent) = 80-89% = 9 points, A (Very Good) = 70-79% = 8 points, B+ (Good) = 60-69% = 7 points, B (Average) = 50-59% = 6 points, C (Below Average) = 40-49% = 5 points, F (Fail) = Below 40% = 0 points.",
         "category": "Examination"},
        {"question": "Can I change my branch/department?",
         "answer": "Branch change is allowed after the first year based on merit (CGPA in first year). Only top 5% students are eligible. Apply through the academic office by June 30. Available seats in the desired branch must be vacant.",
         "category": "Academic"},
    ]
    
    for f in faqs:
        db.add(FAQ(
            question=f["question"], answer=f["answer"],
            category=f["category"], created_by=admin.id
        ))
    db.commit()
    print(f"  [OK] {len(faqs)} FAQs created")
    
    # â”€â”€ Timetable: Computer Science Semester 5 â”€â”€
    cs5_timetable = [
        # Monday
        {"day": "Monday", "subject": "Database Management Systems", "start": "09:00", "end": "10:00", "faculty": "Prof. S. Krishnan", "room": "CS-101"},
        {"day": "Monday", "subject": "Computer Networks", "start": "10:00", "end": "11:00", "faculty": "Prof. A. Reddy", "room": "CS-102"},
        {"day": "Monday", "subject": "Operating Systems", "start": "11:00", "end": "12:00", "faculty": "Prof. M. Gupta", "room": "CS-103"},
        {"day": "Monday", "subject": "Artificial Intelligence", "start": "13:00", "end": "14:00", "faculty": "Dr. R. Kumar", "room": "CS-201"},
        {"day": "Monday", "subject": "DBMS Lab", "start": "14:00", "end": "16:00", "faculty": "Prof. S. Krishnan", "room": "Lab-1"},
        # Tuesday
        {"day": "Tuesday", "subject": "Computer Networks", "start": "09:00", "end": "10:00", "faculty": "Prof. A. Reddy", "room": "CS-102"},
        {"day": "Tuesday", "subject": "Artificial Intelligence", "start": "10:00", "end": "11:00", "faculty": "Dr. R. Kumar", "room": "CS-201"},
        {"day": "Tuesday", "subject": "Web Technologies", "start": "11:00", "end": "12:00", "faculty": "Prof. P. Sharma", "room": "CS-104"},
        {"day": "Tuesday", "subject": "Operating Systems", "start": "13:00", "end": "14:00", "faculty": "Prof. M. Gupta", "room": "CS-103"},
        {"day": "Tuesday", "subject": "CN Lab", "start": "14:00", "end": "16:00", "faculty": "Prof. A. Reddy", "room": "Lab-2"},
        # Wednesday
        {"day": "Wednesday", "subject": "Database Management Systems", "start": "09:00", "end": "10:00", "faculty": "Prof. S. Krishnan", "room": "CS-101"},
        {"day": "Wednesday", "subject": "Operating Systems", "start": "10:00", "end": "11:00", "faculty": "Prof. M. Gupta", "room": "CS-103"},
        {"day": "Wednesday", "subject": "Web Technologies", "start": "11:00", "end": "12:00", "faculty": "Prof. P. Sharma", "room": "CS-104"},
        {"day": "Wednesday", "subject": "Artificial Intelligence", "start": "13:00", "end": "14:00", "faculty": "Dr. R. Kumar", "room": "CS-201"},
        {"day": "Wednesday", "subject": "AI Lab", "start": "14:00", "end": "16:00", "faculty": "Dr. R. Kumar", "room": "Lab-3"},
        # Thursday
        {"day": "Thursday", "subject": "Artificial Intelligence", "start": "09:00", "end": "10:00", "faculty": "Dr. R. Kumar", "room": "CS-201"},
        {"day": "Thursday", "subject": "Computer Networks", "start": "10:00", "end": "11:00", "faculty": "Prof. A. Reddy", "room": "CS-102"},
        {"day": "Thursday", "subject": "Operating Systems", "start": "11:00", "end": "12:00", "faculty": "Prof. M. Gupta", "room": "CS-103"},
        {"day": "Thursday", "subject": "Web Technologies", "start": "13:00", "end": "14:00", "faculty": "Prof. P. Sharma", "room": "CS-104"},
        {"day": "Thursday", "subject": "OS Lab", "start": "14:00", "end": "16:00", "faculty": "Prof. M. Gupta", "room": "Lab-1"},
        # Friday
        {"day": "Friday", "subject": "Database Management Systems", "start": "09:00", "end": "10:00", "faculty": "Prof. S. Krishnan", "room": "CS-101"},
        {"day": "Friday", "subject": "Artificial Intelligence", "start": "10:00", "end": "11:00", "faculty": "Dr. R. Kumar", "room": "CS-201"},
        {"day": "Friday", "subject": "Computer Networks", "start": "11:00", "end": "12:00", "faculty": "Prof. A. Reddy", "room": "CS-102"},
        {"day": "Friday", "subject": "Web Technologies Lab", "start": "13:00", "end": "15:00", "faculty": "Prof. P. Sharma", "room": "Lab-2"},
    ]
    
    for t in cs5_timetable:
        db.add(Timetable(
            department="Computer Science", semester=5,
            day_of_week=t["day"], subject=t["subject"],
            start_time=t["start"], end_time=t["end"],
            faculty_name=t["faculty"], room_number=t["room"]
        ))
    
    # â”€â”€ Timetable: Computer Science Semester 3 â”€â”€
    cs3_timetable = [
        {"day": "Monday", "subject": "Data Structures", "start": "09:00", "end": "10:00", "faculty": "Prof. V. Iyer", "room": "CS-201"},
        {"day": "Monday", "subject": "Digital Logic Design", "start": "10:00", "end": "11:00", "faculty": "Prof. K. Nair", "room": "CS-202"},
        {"day": "Monday", "subject": "Discrete Mathematics", "start": "11:00", "end": "12:00", "faculty": "Prof. L. Menon", "room": "CS-203"},
        {"day": "Monday", "subject": "OOP with Java", "start": "13:00", "end": "14:00", "faculty": "Prof. T. Das", "room": "CS-204"},
        {"day": "Tuesday", "subject": "Data Structures", "start": "09:00", "end": "10:00", "faculty": "Prof. V. Iyer", "room": "CS-201"},
        {"day": "Tuesday", "subject": "OOP with Java", "start": "10:00", "end": "11:00", "faculty": "Prof. T. Das", "room": "CS-204"},
        {"day": "Tuesday", "subject": "DS Lab", "start": "14:00", "end": "16:00", "faculty": "Prof. V. Iyer", "room": "Lab-1"},
        {"day": "Wednesday", "subject": "Digital Logic Design", "start": "09:00", "end": "10:00", "faculty": "Prof. K. Nair", "room": "CS-202"},
        {"day": "Wednesday", "subject": "Discrete Mathematics", "start": "10:00", "end": "11:00", "faculty": "Prof. L. Menon", "room": "CS-203"},
        {"day": "Wednesday", "subject": "Java Lab", "start": "14:00", "end": "16:00", "faculty": "Prof. T. Das", "room": "Lab-2"},
        {"day": "Thursday", "subject": "Data Structures", "start": "09:00", "end": "10:00", "faculty": "Prof. V. Iyer", "room": "CS-201"},
        {"day": "Thursday", "subject": "Digital Logic Design", "start": "10:00", "end": "11:00", "faculty": "Prof. K. Nair", "room": "CS-202"},
        {"day": "Thursday", "subject": "Discrete Mathematics", "start": "11:00", "end": "12:00", "faculty": "Prof. L. Menon", "room": "CS-203"},
        {"day": "Friday", "subject": "OOP with Java", "start": "09:00", "end": "10:00", "faculty": "Prof. T. Das", "room": "CS-204"},
        {"day": "Friday", "subject": "DLD Lab", "start": "14:00", "end": "16:00", "faculty": "Prof. K. Nair", "room": "Lab-3"},
    ]
    
    for t in cs3_timetable:
        db.add(Timetable(
            department="Computer Science", semester=3,
            day_of_week=t["day"], subject=t["subject"],
            start_time=t["start"], end_time=t["end"],
            faculty_name=t["faculty"], room_number=t["room"]
        ))
    
    db.commit()
    print(f"  [OK] {len(cs5_timetable) + len(cs3_timetable)} timetable entries created")
    
    print()
    print("[OK] Database seeded successfully!")
    print()
    print("Initial administrative and student accounts have been created.")
    print("Change all default passwords immediately after initial access.")
    db.close()


if __name__ == "__main__":
    seed()

