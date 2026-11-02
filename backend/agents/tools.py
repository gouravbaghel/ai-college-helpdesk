"""
LangChain tools for the College Helpdesk AI Agent.
These tools can be used with LangGraph's create_react_agent or called directly.
"""
import logging

logger = logging.getLogger(__name__)


def search_college_documents(query: str) -> str:
    """Search the college knowledge base for information about policies, rules, regulations,
    syllabus, fees, attendance, examinations, hostel, scholarships, and other academic information.
    Use this tool when the student asks about official college policies or document-based information."""
    try:
        from backend.rag.rag_chain import ask_rag
        result = ask_rag(query)
        answer = result.get("answer", "No information found.")
        sources = result.get("sources", [])

        if sources:
            source_text = "\n\nSources:"
            for s in sources:
                source_text += f"\n- {s.get('document_name', 'Unknown')} (Page {s.get('page_number', '?')}, Category: {s.get('category', 'General')})"
            answer += source_text

        return answer
    except Exception as e:
        logger.error(f"Error searching documents: {e}")
        return "Sorry, document search is not available right now."


def get_student_timetable(department: str, semester: int = 1, day: str = None) -> str:
    """Get the class timetable/schedule for a specific department and semester.
    Optionally filter by day of the week.
    Use this when students ask about their class schedule, next class, or timetable."""
    from backend.database import SessionLocal
    from backend.models.timetable import Timetable

    db = SessionLocal()
    try:
        query = db.query(Timetable).filter(
            Timetable.department == department,
            Timetable.semester == semester
        )
        if day:
            query = query.filter(Timetable.day_of_week == day)
        tts = query.order_by(Timetable.day_of_week, Timetable.start_time).all()

        if not tts:
            return f"No timetable found for {department} department, semester {semester}."

        result = f"Timetable for {department} - Semester {semester}:\n"
        current_day = ""
        for t in tts:
            if t.day_of_week != current_day:
                current_day = t.day_of_week
                result += f"\n{current_day}:\n"
            result += f"  {t.start_time}-{t.end_time}: {t.subject} | Faculty: {t.faculty_name} | Room: {t.room_number}\n"
        return result
    finally:
        db.close()


def get_latest_notices(limit: int = 5) -> str:
    """Get the latest college notices and announcements.
    Use this when students ask about recent notices, announcements, exam schedules, or important dates."""
    from backend.database import SessionLocal
    from backend.models.notice import Notice

    db = SessionLocal()
    try:
        notices = db.query(Notice).order_by(Notice.created_at.desc()).limit(limit).all()
        if not notices:
            return "No notices found."
        result = "Latest College Notices:\n"
        for n in notices:
            date_str = n.created_at.strftime("%Y-%m-%d") if n.created_at else "Unknown"
            result += f"\n[{n.priority or 'Medium'}] {n.title} ({date_str})\n{n.content}\n"
        return result
    finally:
        db.close()


def search_faq(query: str) -> str:
    """Search the FAQ database for common questions and answers.
    Use this for quick answers to frequently asked questions about college procedures."""
    from backend.database import SessionLocal
    from backend.models.faq import FAQ

    db = SessionLocal()
    try:
        faqs = db.query(FAQ).all()
        if not faqs:
            return "No FAQs found."

        query_lower = query.lower()
        matching = []
        for f in faqs:
            if (query_lower in f.question.lower() or
                query_lower in f.answer.lower() or
                any(word in f.question.lower() for word in query_lower.split())):
                matching.append(f)

        if not matching:
            return "No relevant FAQs found for your question."

        result = "Found following FAQs:\n"
        for f in matching[:3]:
            result += f"Q: {f.question}\nA: {f.answer}\n\n"
        return result
    finally:
        db.close()
