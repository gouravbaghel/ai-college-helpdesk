"""Document management service: upload, process, and manage documents."""
from sqlalchemy.orm import Session
from backend.models.document import Document
from backend.config import settings
from fastapi import HTTPException
import os
import logging
import uuid

logger = logging.getLogger(__name__)


async def process_and_store_document(file, category: str, db: Session, user_id: int):
    """Upload a PDF file, process it for RAG, and save metadata to DB."""
    original_filename = os.path.basename(file.filename or "").strip()
    if not original_filename or not original_filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Please upload a PDF file")

    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    stored_filename = f"{uuid.uuid4().hex}.pdf"
    file_path = os.path.join(settings.UPLOAD_DIR, stored_filename)

    max_file_size = 25 * 1024 * 1024
    content = await file.read(max_file_size + 1)
    if not content.startswith(b"%PDF-"):
        raise HTTPException(status_code=400, detail="The uploaded file is not a valid PDF")
    if len(content) > max_file_size:
        raise HTTPException(status_code=413, detail="PDF files must be 25 MB or smaller")
    with open(file_path, "wb") as buffer:
        buffer.write(content)

    # Process for RAG (lazy import to avoid startup crash)
    chunk_count = 0
    try:
        from backend.rag.document_processor import process_pdf_and_store
        chunk_count = process_pdf_and_store(file_path, original_filename, category)
    except Exception as e:
        logger.error(f"Error processing document for RAG: {e}")
        # File is still saved, just not indexed

    db_doc = Document(
        filename=original_filename,
        file_path=file_path,
        category=category,
        chunk_count=chunk_count,
        uploaded_by=user_id
    )
    db.add(db_doc)
    db.commit()
    db.refresh(db_doc)

    logger.info(f"Document uploaded: {original_filename}, chunks: {chunk_count}")
    message = "File uploaded and indexed successfully" if chunk_count else "File uploaded, but no text chunks were indexed"
    return {"message": message, "doc_id": db_doc.id, "chunks": chunk_count}


def get_all_documents(db: Session):
    """Get all documents from the database."""
    return db.query(Document).order_by(Document.upload_date.desc()).all()


def delete_document(db: Session, doc_id: int):
    """Delete a document from the database, filesystem, and vector store."""
    doc = db.query(Document).filter(Document.id == doc_id).first()
    if doc:
        # Delete from vector store
        try:
            from backend.rag.vector_store import get_vector_store
            vector_store = get_vector_store()
            vector_store.delete_by_document_name(doc.filename)
        except Exception as e:
            logger.warning(f"Could not remove chunks from vector store for {doc.filename}: {e}")

        if os.path.exists(doc.file_path):
            os.remove(doc.file_path)
        db.delete(doc)
        db.commit()
        logger.info(f"Document deleted: {doc.filename}")
        return {"message": "Document deleted successfully"}
    return {"message": "Document not found"}
