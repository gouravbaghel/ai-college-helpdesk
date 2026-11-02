# AI-Powered College Helpdesk & Student Assistant

<div align="center">

**An intelligent, RAG-powered chatbot system for college students and administrators**

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-red.svg)](https://streamlit.io)
[![LangChain](https://img.shields.io/badge/LangChain-Latest-orange.svg)](https://langchain.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

---

## Project Overview

The **AI-Powered College Helpdesk & Student Assistant** is a full-stack web application that uses **Retrieval-Augmented Generation (RAG)** and **AI agents** to help college students get instant, accurate answers to questions about:

- Attendance rules and regulations
- Examination policies and grading
- Fee structure and payment deadlines
- Scholarship information
- Hostel rules and facilities
- Class timetable and schedules
- College notices and announcements
- Frequently asked questions

The system retrieves information from **official college documents** (PDFs) and provides **grounded, citation-backed answers** — it never fabricates information.

---

## Architecture

```
┌──────────────┐     ┌──────────────────┐     ┌───────────────────┐
│   Student /  │     │   Streamlit UI   │     │   FastAPI Backend  │
│   Admin      │────▶│   (Frontend)     │────▶│   (REST API)       │
│   Browser    │     │   Port: 8501     │     │   Port: 8000       │
└──────────────┘     └──────────────────┘     └────────┬──────────┘
                                                        │
                              ┌──────────────────────────┤
                              │                          │
                    ┌─────────▼─────────┐    ┌──────────▼──────────┐
                    │   LangGraph Agent  │    │   SQLite Database   │
                    │   (Tool Router)    │    │   - Users           │
                    └─────────┬─────────┘    │   - Notices         │
                              │              │   - Timetable       │
                    ┌─────────▼─────────┐    │   - FAQs            │
                    │   RAG Pipeline    │    │   - Chat History    │
                    │   - Embed Query   │    │   - Documents       │
                    │   - Vector Search │    │   - Feedback        │
                    │   - Get Context   │    └─────────────────────┘
                    └─────────┬─────────┘
                              │
                    ┌─────────▼─────────┐    ┌─────────────────────┐
                    │   ChromaDB        │    │   Groq LLM API     │
                    │   (Vector Store)  │────▶│   (llama-3.3-70b)  │
                    │   - Embeddings    │    │   Grounded Answer   │
                    │   - Metadata      │    │   + Citations       │
                    └───────────────────┘    └─────────────────────┘
```

### RAG Pipeline Flow

```
College PDF Documents
    → PyMuPDF Text Extraction
    → Text Cleaning & Preprocessing
    → Recursive Character Chunking (1000 chars, 200 overlap)
    → Sentence-Transformer Embeddings (all-MiniLM-L6-v2)
    → ChromaDB Vector Storage (with metadata)
    → Semantic Similarity Search (Top-K retrieval)
    → Context + Query → Groq LLM (llama-3.3-70b)
    → Grounded Answer + Source Citations
```

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| **Backend** | FastAPI, Python 3.10+ |
| **Frontend** | Streamlit |
| **Database** | SQLite (SQLAlchemy ORM) |
| **Vector Store** | ChromaDB |
| **LLM** | Groq API (Llama 3.3 70B) |
| **Embeddings** | sentence-transformers/all-MiniLM-L6-v2 |
| **RAG Framework** | LangChain |
| **Agent Framework** | LangGraph |
| **PDF Processing** | PyMuPDF (fitz) |
| **Authentication** | JWT (python-jose + passlib) |

---

## Features

### Student Features
- **AI Chat Assistant** — Ask questions in natural language and get cited answers
- **Timetable View** — View class schedules by department, semester, and day
- **Notices** — Browse latest college notices and announcements
- **Chat History** — Review past conversations with the AI
- **Profile** — View and manage student profile
- **Feedback** — Rate AI responses for quality improvement

### Admin Features
- **Document Management** — Upload PDFs to expand the AI knowledge base
- **Notice Management** — Create, edit, and delete notices
- **FAQ Management** — Manage frequently asked questions
- **Timetable Management** — Add and manage class schedules
- **Query Monitoring** — View all student queries and AI responses
- **Analytics Dashboard** — System metrics and usage statistics
- **RAG Evaluation** — View AI system performance metrics

### AI Features
- **RAG-based Retrieval** — Searches official college documents
- **Source Citations** — Shows document name, page number for every answer
- **Grounded Answers** — Never fabricates information; says "I don't know" when unsure
- **Intelligent Routing** — Automatically chooses the right tool for each question
- **Conversation Context** — Maintains context within a conversation

---

## Project Structure

```
ai-college-helpdesk/
├── backend/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── config.py               # Configuration (pydantic-settings)
│   ├── database.py             # Database connection setup
│   ├── seed_data.py            # Database seeding script
│   ├── api/
│   │   ├── __init__.py
│   │   ├── auth.py             # Authentication endpoints
│   │   ├── admin.py            # Admin endpoints
│   │   ├── chat.py             # AI chat endpoints
│   │   ├── deps.py             # Shared dependencies
│   │   └── students.py         # Student endpoints
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py             # User model
│   │   ├── document.py         # Document model
│   │   ├── notice.py           # Notice model
│   │   ├── timetable.py        # Timetable model
│   │   ├── faq.py              # FAQ model
│   │   └── chat.py             # Chat & Feedback models
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py             # User Pydantic schemas
│   │   ├── document.py         # Document schemas
│   │   ├── notice.py           # Notice schemas
│   │   ├── timetable.py        # Timetable schemas
│   │   ├── faq.py              # FAQ schemas
│   │   └── chat.py             # Chat schemas
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_service.py     # Authentication logic
│   │   ├── document_service.py # Document CRUD
│   │   ├── notice_service.py   # Notice CRUD
│   │   ├── timetable_service.py# Timetable CRUD
│   │   ├── faq_service.py      # FAQ CRUD
│   │   ├── chat_service.py     # Chat history management
│   │   └── analytics_service.py# Analytics queries
│   ├── rag/
│   │   ├── __init__.py
│   │   ├── embeddings.py       # Embedding model setup
│   │   ├── vector_store.py     # ChromaDB operations
│   │   ├── document_processor.py# PDF extraction & chunking
│   │   ├── retriever.py        # Semantic search
│   │   └── rag_chain.py        # RAG chain with LLM
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── tools.py            # Agent tools
│   │   └── college_agent.py    # LangGraph agent
│   └── utils/
│       ├── __init__.py
│       ├── logger.py           # Logging setup
│       └── helpers.py          # Utility functions
├── frontend/
│   ├── app.py                  # Main Streamlit app
│   ├── pages/
│   │   ├── __init__.py
│   │   ├── login.py            # Login/Register page
│   │   ├── student_dashboard.py# Student dashboard
│   │   ├── ai_assistant.py     # AI chat interface
│   │   ├── notices.py          # Notice viewer
│   │   ├── timetable.py        # Timetable viewer
│   │   ├── chat_history.py     # Chat history
│   │   ├── profile.py          # Student profile
│   │   ├── admin_dashboard.py  # Admin analytics
│   │   ├── admin_documents.py  # Document management
│   │   ├── admin_notices.py    # Notice management
│   │   ├── admin_faqs.py       # FAQ management
│   │   ├── admin_timetable.py  # Timetable management
│   │   ├── admin_queries.py    # Query viewer
│   │   └── admin_evaluation.py # RAG evaluation
│   ├── components/
│   │   ├── __init__.py
│   │   ├── sidebar.py          # Navigation sidebar
│   │   ├── chat_message.py     # Chat message component
│   │   ├── header.py           # Page header
│   │   ├── cards.py            # Card components
│   │   └── styles.py           # CSS styles
│   └── utils/
│       ├── __init__.py
│       ├── api.py              # API client
│       └── session.py          # Session management
├── data/
│   ├── documents/              # Generated sample PDFs
│   ├── sample_data/
│   │   ├── faqs.json
│   │   ├── notices.json
│   │   ├── students.json
│   │   └── timetable.json
│   └── generate_sample_pdfs.py # PDF generator
├── tests/
│   ├── __init__.py
│   ├── test_api.py             # API tests
│   └── test_rag_evaluation.py  # RAG evaluation
├── .env.example                # Environment template
├── .gitignore
├── README.md
├── requirements.txt
├── run_backend.py              # Backend launcher
├── run_frontend.py             # Frontend launcher
└── setup.py                    # Project setup script
```

---

## Prerequisites

- **Python 3.10+** installed
- **pip** package manager
- **Groq API Key** (free at [console.groq.com](https://console.groq.com/keys))
- 4GB+ RAM (for embedding model)
- Internet connection (for LLM API calls)

---

## Installation

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd ai-college-helpdesk
```

### Step 2: Create Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment

```bash
# Copy the example environment file
copy .env.example .env    # Windows
cp .env.example .env      # Linux/macOS

# Edit .env and add your Groq API key
# GROQ_API_KEY=your_key_here
```

### Step 5: Run Automated Setup

```bash
python setup.py
```

This will:
1. Create `.env` from template
2. Generate sample PDF documents
3. Seed the database with demo data
4. Ingest documents into the vector store

### Step 6: Start the Backend

```bash
python run_backend.py
```

The API will be available at `http://localhost:8000` (Docs at `/docs`)

### Step 7: Start the Frontend (New Terminal)

```bash
python run_frontend.py
```

The app will be available at `http://localhost:8501`

---

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GROQ_API_KEY` | Your Groq API key | Required |
| `JWT_SECRET_KEY` | Secret key for JWT tokens | Change in production |
| `DATABASE_URL` | SQLite database path | `sqlite:///./college_helpdesk.db` |
| `CHROMA_PERSIST_DIR` | ChromaDB storage path | `./chroma_db` |
| `EMBEDDING_MODEL` | HuggingFace embedding model | `sentence-transformers/all-MiniLM-L6-v2` |
| `LLM_MODEL` | Groq LLM model name | `llama-3.3-70b-versatile` |
| `LLM_TEMPERATURE` | LLM temperature (0-1) | `0.1` |
| `CHUNK_SIZE` | Text chunk size for RAG | `1000` |
| `CHUNK_OVERLAP` | Chunk overlap | `200` |
| `TOP_K_RESULTS` | Number of retrieved chunks | `5` |

---

## Usage Guide

### Student Workflow

1. **Login** with your registered student account
2. Navigate to **AI Assistant**
3. Ask questions like:
   - "What is the minimum attendance required for exams?"
   - "What is the fee structure for B.Tech?"
   - "Show me the latest notices"
   - "When is my next DBMS class?"
4. View cited sources below each answer
5. Browse **Notices** and **Timetable** pages
6. Review past conversations in **Chat History**

### Admin Workflow

1. **Login** with your administrator credentials
2. View system metrics on **Admin Dashboard**
3. Upload new PDFs in **Document Management**
4. Create notices in **Notice Management**
5. Add FAQs in **FAQ Management**
6. Manage timetable in **Timetable Management**
7. Monitor queries in **User Queries**
8. Check AI performance in **Evaluation**

---

## AI / RAG Architecture

### How It Works

1. **Document Ingestion**: When a PDF is uploaded, PyMuPDF extracts text page by page. The text is cleaned and split into overlapping chunks using LangChain's RecursiveCharacterTextSplitter.

2. **Embedding**: Each chunk is converted into a 384-dimensional vector using the `all-MiniLM-L6-v2` sentence transformer model.

3. **Storage**: Vectors and metadata (document name, page number, category) are stored in ChromaDB.

4. **Query Processing**: When a student asks a question, the AI agent first determines the appropriate tool:
   - **Document Search** → RAG pipeline for policy/rule questions
   - **Timetable Tool** → Database query for schedule questions
   - **Notice Tool** → Database query for announcement questions
   - **FAQ Tool** → FAQ database search for common questions

5. **RAG Retrieval**: For document-based queries, the question is embedded and the top-K most similar chunks are retrieved from ChromaDB.

6. **Answer Generation**: The retrieved context is sent to the Groq LLM with a grounding system prompt that instructs it to ONLY use the provided context and explicitly state when information is unavailable.

7. **Citation**: Source document names and page numbers from the retrieved chunks are returned alongside the answer.

### AI Safety Rules

- Answers are grounded in retrieved documents
- Sources are real and traceable
- "I don't know" is the response when context is insufficient
- System prompts and API keys are never exposed
- No fabrication of college policies

---

## API Documentation

The FastAPI backend auto-generates interactive API docs at:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### Key Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/api/auth/register` | Register user | No |
| POST | `/api/auth/login` | Login | No |
| GET | `/api/auth/me` | Get current user | Yes |
| POST | `/api/chat/ask` | Ask AI question | Yes |
| GET | `/api/chat/history` | Get conversations | Yes |
| GET | `/api/student/timetable` | Get timetable | Yes |
| GET | `/api/student/notices` | Get notices | Yes |
| POST | `/api/admin/documents/upload` | Upload document | Admin |
| GET | `/api/admin/analytics` | Get analytics | Admin |
| GET | `/api/admin/queries` | View queries | Admin |

---

## Security & Access Control

Default administrative and student accounts are provisioned during database initialization.

> **Important**: In production, change all initial passwords immediately and ensure that `JWT_SECRET_KEY` is configured securely in the environment.

---

## RAG Evaluation

Run the evaluation suite to measure AI performance:

```bash
python -m tests.test_rag_evaluation
```

This generates `evaluation_results.json` with metrics:
- **Retrieval Accuracy** — Was the correct document retrieved?
- **Answer Relevance** — Does the answer contain expected keywords?
- **Citation Accuracy** — Are the cited sources correct?
- **Response Latency** — How fast are responses?
- **Unanswered Count** — How many questions couldn't be answered?

View results in the admin dashboard under **Evaluation**.

---

## Running Tests

```bash
# API tests
python -m pytest tests/test_api.py -v

# RAG evaluation
python -m tests.test_rag_evaluation
```

---

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- [LangChain](https://langchain.com) — RAG framework
- [Groq](https://groq.com) — Fast LLM inference
- [ChromaDB](https://www.trychroma.com) — Vector database
- [FastAPI](https://fastapi.tiangolo.com) — Backend framework
- [Streamlit](https://streamlit.io) — Frontend framework
- [Sentence Transformers](https://www.sbert.net) — Embedding models

---

<div align="center">
  <p><strong>AI-Powered College Helpdesk & Student Assistant</strong></p>
  <p><em>Enterprise-grade RAG and agentic information system</em></p>
</div>
