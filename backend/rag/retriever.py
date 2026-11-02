"""Document retriever using Hybrid Search (ChromaDB vector similarity + BM25 keyword re-ranking)."""
import logging
import re
from typing import List
from langchain_core.documents import Document
from backend.config import settings

logger = logging.getLogger(__name__)

STOPWORDS = {
    'a', 'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and', 'any', 'are',
    'as', 'at', 'be', 'because', 'been', 'before', 'being', 'below', 'between', 'both', 'but',
    'by', 'can', 'could', 'did', 'do', 'does', 'doing', 'down', 'during', 'each', 'few', 'for',
    'from', 'further', 'had', 'has', 'have', 'having', 'he', 'her', 'here', 'hers', 'herself',
    'him', 'himself', 'his', 'how', 'i', 'if', 'in', 'into', 'is', 'it', 'its', 'itself', 'just',
    'me', 'more', 'most', 'my', 'myself', 'no', 'nor', 'not', 'now', 'of', 'off', 'on', 'once',
    'only', 'or', 'other', 'our', 'ours', 'ourselves', 'out', 'over', 'own', 'same', 'she',
    'should', 'so', 'some', 'such', 'than', 'that', 'the', 'their', 'theirs', 'them', 'themselves',
    'then', 'there', 'these', 'they', 'this', 'those', 'through', 'to', 'too', 'under', 'until',
    'up', 'very', 'was', 'we', 'were', 'what', 'when', 'where', 'which', 'while', 'who', 'whom',
    'why', 'with', 'would', 'you', 'your', 'yours', 'yourself', 'yourselves'
}


def retrieve_documents(query: str, k: int = None) -> List[Document]:
    """
    Retrieve the most relevant documents for a query using Hybrid Search:
    Combines dense ChromaDB vector similarity with sparse keyword matching.
    """
    if k is None:
        k = settings.TOP_K_RESULTS

    try:
        from backend.rag.vector_store import get_vector_store
        vector_store = get_vector_store()
        total_items = vector_store.count()
        if total_items == 0:
            logger.info("Vector store has 0 documents.")
            return []

        # Retrieve a broad candidate pool from vector store (up to 35 items)
        candidate_k = min(35, total_items)
        results = vector_store.collection.query(
            query_texts=[query],
            n_results=candidate_k
        )

        if not results or not results["documents"] or not results["documents"][0]:
            return []

        docs_list = results["documents"][0]
        meta_list = results["metadatas"][0]
        dist_list = results["distances"][0] if "distances" in results and results["distances"] else [1.0] * len(docs_list)

        # Extract meaningful query keywords
        raw_words = re.findall(r'\b[a-zA-Z0-9_\-\.]{2,}\b', query.lower())
        query_keywords = [w for w in raw_words if w not in STOPWORDS]

        scored_candidates = []
        for doc_text, meta, dist in zip(docs_list, meta_list, dist_list):
            doc_lower = doc_text.lower()
            # Vector score (normalized 0 to 1, higher is better)
            vector_score = 1.0 / (1.0 + max(0.0, float(dist)))

            # Keyword matching score
            keyword_score = 0.0
            for kw in query_keywords:
                if kw in doc_lower:
                    # Exact word match
                    keyword_score += 1.5
                    # Extra boost if keyword is in the document category or title
                    cat = str(meta.get("category", "")).lower()
                    doc_name = str(meta.get("document_name", "")).lower()
                    if kw in cat or kw in doc_name:
                        keyword_score += 1.0

            hybrid_score = vector_score + keyword_score
            doc_obj = Document(page_content=doc_text, metadata=meta or {})
            scored_candidates.append((hybrid_score, doc_obj))

        # Sort descending by hybrid score
        scored_candidates.sort(key=lambda x: x[0], reverse=True)
        top_docs = [item[1] for item in scored_candidates[:k]]

        logger.info(f"Hybrid retrieval returned {len(top_docs)} documents for query: {query[:50]}...")
        return top_docs

    except Exception as e:
        logger.error(f"Error in hybrid retrieval: {e}")
        return []
