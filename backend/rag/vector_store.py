"""ChromaDB native vector store setup for College Helpdesk.
Directly uses chromadb.PersistentClient with LangChain Document compatibility.
"""
import logging
import uuid
from typing import List, Optional
from langchain_core.documents import Document
from backend.config import settings
from backend.rag.embeddings import get_embeddings_model

logger = logging.getLogger(__name__)
_vector_store_instance = None


class CollegeVectorStore:
    """Wrapper around ChromaDB PersistentClient providing LangChain Document interface."""

    def __init__(self, persist_directory: str = "./chroma_db", collection_name: str = "college_documents"):
        import chromadb
        self.persist_directory = persist_directory
        self.collection_name = collection_name
        self.client = chromadb.PersistentClient(path=self.persist_directory)
        self.embedding_fn = get_embeddings_model()
        
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            embedding_function=self.embedding_fn,
            metadata={"description": "Rajiv Gandhi Institute of Technology Knowledge Base"}
        )
        logger.info(f"Connected to ChromaDB collection '{self.collection_name}' ({self.collection.count()} items).")

    def add_documents(self, documents: List[Document]) -> List[str]:
        """Add LangChain Document chunks to ChromaDB."""
        if not documents:
            return []

        ids = []
        texts = []
        metadatas = []

        for i, doc in enumerate(documents):
            doc_name = doc.metadata.get("document_name", "doc")
            page_num = doc.metadata.get("page_number", 0)
            chunk_idx = doc.metadata.get("chunk_index", i)
            # Create deterministic ID to prevent duplicate insertions
            chunk_id = f"{doc_name}_p{page_num}_c{chunk_idx}_{uuid.uuid4().hex[:6]}"
            ids.append(chunk_id)
            texts.append(doc.page_content)
            # Chroma metadata values must be str, int, float, or bool
            clean_meta = {}
            for k, v in doc.metadata.items():
                if isinstance(v, (str, int, float, bool)):
                    clean_meta[k] = v
                else:
                    clean_meta[k] = str(v)
            metadatas.append(clean_meta)

        self.collection.add(
            ids=ids,
            documents=texts,
            metadatas=metadatas
        )
        logger.info(f"Added {len(documents)} document chunks to ChromaDB.")
        return ids

    def similarity_search(self, query: str, k: int = 5) -> List[Document]:
        """Search the ChromaDB collection for chunks most relevant to query."""
        total_items = self.collection.count()
        if total_items == 0:
            logger.info("ChromaDB collection is empty.")
            return []

        actual_k = min(k, total_items)
        results = self.collection.query(
            query_texts=[query],
            n_results=actual_k
        )

        docs = []
        if results and "documents" in results and results["documents"]:
            doc_list = results["documents"][0]
            meta_list = results.get("metadatas", [[]])[0]
            for text, meta in zip(doc_list, meta_list):
                docs.append(Document(page_content=text, metadata=meta or {}))

        return docs

    def count(self) -> int:
        return self.collection.count()

    def delete_by_document_name(self, filename: str):
        """Delete all chunks belonging to a specific document."""
        try:
            self.collection.delete(where={"document_name": filename})
            logger.info(f"Deleted chunks for document {filename} from ChromaDB.")
        except Exception as e:
            logger.error(f"Error deleting chunks for {filename}: {e}")


def get_vector_store():
    """Get singleton CollegeVectorStore instance."""
    global _vector_store_instance
    if _vector_store_instance is None:
        _vector_store_instance = CollegeVectorStore(
            persist_directory=settings.CHROMA_PERSIST_DIR,
            collection_name="college_documents"
        )
    return _vector_store_instance
