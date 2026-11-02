"""
AI Agent for the College Helpdesk system.
Routes user queries to the appropriate tool based on intent.
"""
import logging
import re
from datetime import datetime

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are an AI assistant for Rajiv Gandhi Institute of Technology (RGIT).
You help students with questions about college information.

You have access to the following tools:
1. search_college_documents - Search uploaded college PDFs for official policies, rules, regulations
2. get_student_timetable - Get class schedules by department and semester
3. get_latest_notices - Get recent college notices and announcements
4. search_faq - Search frequently asked questions

Decide which tool is most appropriate based on the question:
- For questions about policies, rules, regulations, syllabus, fees, attendance, exams, hostel, scholarships -> use search_college_documents
- For questions about class schedule, next class, timetable -> use get_student_timetable
- For questions about latest notices, announcements, important dates -> use get_latest_notices
- For common/general questions -> use search_faq first, then search_college_documents if needed

Always provide helpful, accurate answers. If you cannot find the information, say so clearly.
Do NOT fabricate information. Keep answers concise but complete."""


def generate_response(query: str, user_id: int, db) -> dict:
    """Generate a response to a user query using the appropriate tool."""
    query_lower = query.lower()

    try:
        # Route to appropriate tool based on query intent
        if any(word in query_lower for word in ["timetable", "schedule", "class", "next class", "when is my", "time slot"]):
            return _handle_timetable_query(query, query_lower, db, user_id)

        elif any(word in query_lower for word in ["notice", "announcement", "latest notice", "recent notice", "exam notice", "important date"]):
            return _handle_notice_query(query, db)

        elif any(word in query_lower for word in ["faq", "frequently asked", "common question"]):
            return _handle_faq_query(query, db)

        else:
            # Default: Use RAG document search
            return _handle_rag_query(query)

    except Exception as e:
        logger.error(f"Agent error: {e}")
        # Fallback to RAG
        try:
            return _handle_rag_query(query)
        except Exception as e2:
            logger.error(f"RAG fallback error: {e2}")
            return {
                "answer": "I'm sorry, I encountered an error while processing your question. Please ensure the system is properly configured with an API key.",
                "sources": []
            }


def _handle_timetable_query(query: str, query_lower: str, db, user_id: int) -> dict:
    """Handle timetable-related queries by searching the database."""
    from backend.models.timetable import Timetable
    from backend.models.user import User

    student = db.query(User).filter(User.id == user_id).first()
    department = (student.department if student else None) or "Computer Science"
    semester = (student.semester if student else None) or 5
    day = None

    days_map = {
        "monday": "Monday", "tuesday": "Tuesday", "wednesday": "Wednesday",
        "thursday": "Thursday", "friday": "Friday", "saturday": "Saturday"
    }
    for d_key, d_val in days_map.items():
        if d_key in query_lower:
            day = d_val
            break

    # Try to extract semester
    sem_match = re.search(r'semester\s*(\d+)', query_lower)
    if sem_match:
        semester = int(sem_match.group(1))

    query_obj = db.query(Timetable).filter(
        Timetable.department == department,
        Timetable.semester == semester
    )
    if day:
        query_obj = query_obj.filter(Timetable.day_of_week == day)

    results = query_obj.order_by(Timetable.start_time).all()

    if not results:
        return {
            "answer": f"I couldn't find any timetable entries for {department} Semester {semester}" + (f" on {day}" if day else "") + ". Please check with the administration.",
            "sources": []
        }

    answer = f"**Timetable for {department} - Semester {semester}**" + (f" ({day})" if day else "") + ":\n\n"
    current_day = None
    for t in results:
        if not day and t.day_of_week != current_day:
            current_day = t.day_of_week
            answer += f"\n**{current_day}:**\n"
        answer += f"- {t.start_time} - {t.end_time}: **{t.subject}** | {t.faculty_name} | Room {t.room_number}\n"

    return {"answer": answer, "sources": []}


def _handle_notice_query(query: str, db) -> dict:
    """Handle notice-related queries by searching the database."""
    from backend.models.notice import Notice

    notices = db.query(Notice).filter(
        (Notice.expires_at.is_(None)) | (Notice.expires_at >= datetime.utcnow())
    ).order_by(Notice.created_at.desc()).limit(5).all()

    if not notices:
        return {"answer": "There are no notices available at the moment.", "sources": []}

    answer = "**Latest College Notices:**\n\n"
    for n in notices:
        priority_label = f"[{n.priority}]" if n.priority else "[Notice]"
        date_str = n.created_at.strftime("%Y-%m-%d") if n.created_at else "Unknown"
        answer += f"{priority_label} **{n.title}** ({n.category})\n"
        answer += f"   {n.content[:200]}{'...' if len(n.content) > 200 else ''}\n"
        answer += f"   _Posted: {date_str}_\n\n"

    return {"answer": answer, "sources": []}


def _handle_faq_query(query: str, db) -> dict:
    """Handle FAQ queries by searching the database."""
    from backend.models.faq import FAQ

    faqs = db.query(FAQ).all()

    if not faqs:
        return {"answer": "No FAQs are available at the moment.", "sources": []}

    # Simple keyword matching
    query_words = set(query.lower().split())
    scored_faqs = []
    for faq in faqs:
        faq_words = set(faq.question.lower().split())
        overlap = len(query_words & faq_words)
        if overlap > 0:
            scored_faqs.append((overlap, faq))

    scored_faqs.sort(key=lambda x: x[0], reverse=True)

    if scored_faqs:
        best_faq = scored_faqs[0][1]
        answer = f"**Q: {best_faq.question}**\n\n{best_faq.answer}"
        if len(scored_faqs) > 1:
            answer += "\n\n**Related FAQs:**\n"
            for _, faq in scored_faqs[1:3]:
                answer += f"- {faq.question}\n"
        return {"answer": answer, "sources": []}

    # If no match, list some FAQs
    answer = "I couldn't find an exact match. Here are some common questions:\n\n"
    for faq in faqs[:5]:
        answer += f"- **{faq.question}**\n"
    return {"answer": answer, "sources": []}


def _handle_rag_query(query: str) -> dict:
    """Handle document search queries using the RAG pipeline."""
    try:
        from backend.rag.rag_chain import ask_rag
        return ask_rag(query)
    except ImportError as e:
        logger.error(f"RAG dependencies not available: {e}")
        return {
            "answer": "The AI document search is not available. Please ensure all dependencies are installed (langchain, chromadb, sentence-transformers, langchain-groq) and GROQ_API_KEY is set in your .env file.",
            "sources": []
        }
