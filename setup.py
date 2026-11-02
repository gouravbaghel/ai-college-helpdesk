"""
Setup script for AI-Powered College Helpdesk & Student Assistant.
Initializes the environment, generates sample PDFs, seeds the database, 
and ingests documents into the vector store.

Usage: python setup.py
"""
import os
import sys
import shutil
import subprocess

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

def create_env_file():
    """Create .env from .env.example if it doesn't exist."""
    env_file = os.path.join(PROJECT_ROOT, ".env")
    env_example = os.path.join(PROJECT_ROOT, ".env.example")
    
    if os.path.exists(env_file):
        print("[OK] .env file already exists")
        return
    
    if os.path.exists(env_example):
        shutil.copy(env_example, env_file)
        print("[OK] Created .env from .env.example")
        print("  [INFO] Please edit .env and add your GROQ_API_KEY")
    else:
        with open(env_file, "w") as f:
            f.write("""# AI-Powered College Helpdesk Configuration
GROQ_API_KEY=your_groq_api_key_here
JWT_SECRET_KEY=your-super-secret-key-change-in-production
DATABASE_URL=sqlite:///./college_helpdesk.db
CHROMA_PERSIST_DIR=./chroma_db
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
LLM_MODEL=llama-3.3-70b-versatile
LLM_TEMPERATURE=0.1
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
TOP_K_RESULTS=5
UPLOAD_DIR=./uploads
""")
        print("[OK] Created .env file")
        print("  [INFO] Please edit .env and add your GROQ_API_KEY")

def generate_sample_pdfs():
    """Generate sample PDF documents."""
    pdf_script = os.path.join(PROJECT_ROOT, "data", "generate_sample_pdfs.py")
    docs_dir = os.path.join(PROJECT_ROOT, "data", "documents")
    
    if os.path.exists(docs_dir) and os.listdir(docs_dir):
        print("[OK] Sample PDFs already exist")
        return
    
    if os.path.exists(pdf_script):
        print("  Generating sample PDFs...")
        subprocess.run([sys.executable, pdf_script], cwd=PROJECT_ROOT)
        print("[OK] Sample PDFs generated")
    else:
        print("  [INFO] PDF generation script not found at:", pdf_script)
        print("    Skipping PDF generation.")

def seed_database():
    """Seed the database with demo data."""
    db_file = os.path.join(PROJECT_ROOT, "college_helpdesk.db")
    
    if os.path.exists(db_file):
        print("[OK] Database already exists")
        return
    
    print("  Seeding database...")
    sys.path.insert(0, PROJECT_ROOT)
    try:
        from backend.seed_data import seed
        seed()
        print("[OK] Database seeded")
    except Exception as e:
        print(f"  [INFO] Error seeding database: {e}")
        print("    You can seed manually later with: python -m backend.seed_data")

def ingest_documents():
    """Ingest sample PDFs into the vector store."""
    chroma_dir = os.path.join(PROJECT_ROOT, "chroma_db")
    docs_dir = os.path.join(PROJECT_ROOT, "data", "documents")
    
    if os.path.exists(chroma_dir) and os.listdir(chroma_dir):
        print("[OK] Vector store already has data")
        return
    
    if not os.path.exists(docs_dir):
        print("  [INFO] No documents directory found. Skipping ingestion.")
        return
    
    pdf_files = [f for f in os.listdir(docs_dir) if f.endswith(".pdf")]
    if not pdf_files:
        print("  [INFO] No PDF files found in data/documents/. Skipping ingestion.")
        return
    
    print(f"  Ingesting {len(pdf_files)} documents...")
    sys.path.insert(0, PROJECT_ROOT)
    
    try:
        from backend.rag.document_processor import process_pdf_and_store
        
        for pdf_file in pdf_files:
            file_path = os.path.join(docs_dir, pdf_file)
            # Determine category from filename
            category = "General"
            name_lower = pdf_file.lower()
            if "attendance" in name_lower:
                category = "Attendance"
            elif "examination" in name_lower or "exam" in name_lower:
                category = "Examination"
            elif "fee" in name_lower:
                category = "Fees"
            elif "hostel" in name_lower:
                category = "Hostel"
            elif "scholarship" in name_lower:
                category = "Scholarship"
            elif "academic" in name_lower or "calendar" in name_lower:
                category = "Academic Calendar"
            elif "syllabus" in name_lower:
                category = "Syllabus"
            
            print(f"    Processing: {pdf_file} (Category: {category})")
            chunk_count = process_pdf_and_store(file_path, pdf_file, category)
            print(f"    -> {chunk_count} chunks created")
        
        # Also record documents in the database
        try:
            from backend.database import SessionLocal
            from backend.models.document import Document
            import datetime
            
            db = SessionLocal()
            for pdf_file in pdf_files:
                file_path = os.path.join(docs_dir, pdf_file)
                name_lower = pdf_file.lower()
                category = "General"
                if "attendance" in name_lower: category = "Attendance"
                elif "examination" in name_lower: category = "Examination"
                elif "fee" in name_lower: category = "Fees"
                elif "hostel" in name_lower: category = "Hostel"
                elif "scholarship" in name_lower: category = "Scholarship"
                elif "academic" in name_lower: category = "Academic Calendar"
                
                existing = db.query(Document).filter(Document.filename == pdf_file).first()
                if not existing:
                    doc = Document(
                        filename=pdf_file,
                        file_path=file_path,
                        category=category,
                        uploaded_by=1  # admin user
                    )
                    db.add(doc)
            db.commit()
            db.close()
        except Exception as e:
            print(f"    Note: Could not record documents in DB: {e}")
        
        print("[OK] Documents ingested into vector store")
    except Exception as e:
        print(f"  [INFO] Error ingesting documents: {e}")
        print("    You can ingest manually later through the admin dashboard.")

def main():
    # All configured paths are project-relative; setup must behave the same
    # regardless of the caller's current working directory.
    os.chdir(PROJECT_ROOT)
    print("=" * 60)
    print("  AI-Powered College Helpdesk - Setup")
    print("=" * 60)
    print()
    
    # Step 1: Create .env
    print("[1/4] Setting up environment...")
    create_env_file()
    print()
    
    # Step 2: Generate sample PDFs
    print("[2/4] Generating sample documents...")
    generate_sample_pdfs()
    print()
    
    # Step 3: Seed database
    print("[3/4] Seeding database...")
    seed_database()
    print()
    
    # Step 4: Ingest documents
    print("[4/4] Ingesting documents into vector store...")
    ingest_documents()
    print()
    
    print("=" * 60)
    print("  Setup Complete!")
    print("=" * 60)
    print()
    print("Next steps:")
    print("  1. Edit .env and set your GROQ_API_KEY")
    print("     Get one free at: https://console.groq.com/keys")
    print()
    print("  2. Start the backend:")
    print("     python run_backend.py")
    print()
    print("  3. Start the frontend (in a new terminal):")
    print("     python run_frontend.py")
    print()
    print("  4. Open http://localhost:8501 in your browser")
    print()
    print("Initial accounts were provisioned during setup.")
    print("Change all default passwords immediately after initial access.")
    print()

if __name__ == "__main__":
    main()
