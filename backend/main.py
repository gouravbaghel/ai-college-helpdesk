import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.database import engine, Base
from backend.api import auth, students, admin, chat

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Creating database tables...")
    import backend.models.user
    import backend.models.document
    import backend.models.notice
    import backend.models.timetable
    import backend.models.faq
    import backend.models.chat
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created.")
    yield
    # Shutdown
    logger.info("Shutting down...")

app = FastAPI(
    title="AI-Powered College Helpdesk API",
    description="Backend API for the AI-Powered College Helpdesk & Student Assistant",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(students.router, prefix="/api/student", tags=["Student"])
app.include_router(admin.router, prefix="/api/admin", tags=["Admin"])
app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])

@app.get("/")
def root():
    return {"message": "Welcome to AI-Powered College Helpdesk API", "docs": "/docs"}

@app.get("/health")
def health():
    return {"status": "healthy"}
