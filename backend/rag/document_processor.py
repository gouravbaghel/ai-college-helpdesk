"""PDF document processor for the RAG pipeline.
Extracts text from PDFs, cleans it, chunks it, and stores in the vector store.
"""
import re
import logging

logger = logging.getLogger(__name__)


def clean_text(text: str) -> str:
    """Clean extracted text by normalizing whitespace."""
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    return text


def extract_text_from_pdf(file_path: str):
    """
    Extract text and page numbers from a PDF file using pypdf or PyMuPDF.
    Returns a list of dicts: [{'page_number': 1, 'text': '...'}]
    """
    pages_data = []
    
    # Try PyMuPDF first
    try:
        import pymupdf as fitz
        use_fitz = True
    except ImportError:
        try:
            import fitz
            use_fitz = True
        except ImportError:
            use_fitz = False

    if use_fitz:
        try:
            doc = fitz.open(file_path)
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                text = clean_text(page.get_text())
                if text:
                    pages_data.append({"page_number": page_num + 1, "text": text})
            doc.close()
            return pages_data
        except Exception as e:
            logger.warning(f"PyMuPDF failed to read {file_path}: {e}. Falling back to pypdf.")

    # Fallback to pypdf
    try:
        import pypdf
        reader = pypdf.PdfReader(file_path)
        for page_num, page in enumerate(reader.pages):
            text = clean_text(page.extract_text() or "")
            if text:
                pages_data.append({"page_number": page_num + 1, "text": text})
        return pages_data
    except Exception as e:
        logger.error(f"Error reading PDF {file_path} with pypdf: {e}")
        return []


def process_pdf_and_store(file_path: str, filename: str, category: str = "General") -> int:
    """
    Process a PDF file: extract text, chunk it, generate embeddings, store in vector DB.
    Returns the number of chunks created.
    """
    try:
        from langchain_text_splitters import RecursiveCharacterTextSplitter
        from langchain_core.documents import Document
    except ImportError:
        logger.error("langchain-text-splitters or langchain-core is not installed.")
        return 0

    from backend.config import settings

    pages_data = extract_text_from_pdf(file_path)
    if not pages_data:
        logger.warning(f"No text extracted from {filename}")
        return 0

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.CHUNK_SIZE,
        chunk_overlap=settings.CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " ", ""]
    )

    documents = []
    for item in pages_data:
        page_num = item["page_number"]
        text = item["text"]
        chunks = text_splitter.split_text(text)
        for i, chunk in enumerate(chunks):
            documents.append(
                Document(
                    page_content=chunk,
                    metadata={
                        "document_name": filename,
                        "page_number": page_num,
                        "chunk_index": i,
                        "category": category,
                        "source": filename
                    }
                )
            )

    if documents:
        try:
            from backend.rag.vector_store import get_vector_store
            vector_store = get_vector_store()
            vector_store.add_documents(documents)
            logger.info(f"Processed {filename}: {len(documents)} chunks stored.")
        except Exception as e:
            logger.error(f"Error storing documents in vector store: {e}")
            return 0

    return len(documents)
