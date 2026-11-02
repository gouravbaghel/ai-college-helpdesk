"""Embedding model loader for College Helpdesk.
Supports:
1. ChromaDB's built-in DefaultEmbeddingFunction (ONNX all-MiniLM-L6-v2)
2. Fast fallback Semantic Hashing Embeddings (unit-normalized 384-dim vectors)
"""
import hashlib
import logging
import math
import re
from typing import List, Any

logger = logging.getLogger(__name__)
_embeddings = None

def _deterministic_hash(s: str) -> int:
    """Deterministic hash function using MD5 (stable across Python processes)."""
    return int.from_bytes(hashlib.md5(s.encode("utf-8")).digest()[:4], "little")


from chromadb.api.types import Documents, EmbeddingFunction, Embeddings


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


class FallbackHashEmbeddings(EmbeddingFunction[Documents]):
    """
    Lightweight 384-dimensional semantic-hash embedding function with stopword removal.
    Provides fast, offline vector search using word and subword n-grams
    with L2-normalization so cosine distance in ChromaDB works reliably.
    """
    def __init__(self, dim: int = 384):
        self.dim = dim

    def name(self) -> str:
        return "fallback_hash_embedding_v2"

    def _embed_one(self, text: str) -> List[float]:
        raw_tokens = re.findall(r'\b[a-zA-Z0-9_\-\.]{2,}\b', text.lower())
        tokens = [t for t in raw_tokens if t not in STOPWORDS]
        vec = [0.0] * self.dim
        if not tokens:
            tokens = raw_tokens
        if not tokens:
            return vec

        for token in tokens:
            # Whole word hash - deterministic across processes
            h = _deterministic_hash(token) % self.dim
            vec[h] += 3.0
            # Character trigram hashes for subword matching
            clean_tok = re.sub(r'[^a-z0-9]', '', token)
            if len(clean_tok) >= 3:
                for i in range(len(clean_tok) - 2):
                    trigram = clean_tok[i:i+3]
                    h_tri = (_deterministic_hash(trigram) * 31) % self.dim
                    vec[h_tri] += 0.5

        # L2 normalize
        norm = math.sqrt(sum(x * x for x in vec))
        if norm > 0:
            vec = [x / norm for x in vec]
        return vec

    def __call__(self, input: Documents) -> Embeddings:
        return [self._embed_one(t) for t in input]

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return [self._embed_one(t) for t in texts]

    def embed_query(self, input: Any) -> Any:
        if isinstance(input, list):
            return [self._embed_one(t) for t in input]
        return self._embed_one(str(input))


class ChromaEmbeddingWrapper(EmbeddingFunction[Documents]):
    """Wraps an embedding function for LangChain and Chroma compatibility."""
    def __init__(self, ef):
        self.ef = ef

    def name(self) -> str:
        if hasattr(self.ef, "name") and callable(self.ef.name):
            return self.ef.name()
        return "chroma_default"

    def __call__(self, input: Documents) -> Embeddings:
        return self.ef(input)

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return self.ef(texts)

    def embed_query(self, input: Any) -> Any:
        if isinstance(input, list):
            return self.ef(input)
        res = self.ef([str(input)])
        return res[0] if res else []

    def embed_query(self, text: str) -> List[float]:
        return self.ef([text])[0]

    def __call__(self, input: List[str]) -> List[List[float]]:
        return self.ef(input)


def get_embeddings_model():
    """Get or create the embeddings model instance (singleton)."""
    global _embeddings
    if _embeddings is not None:
        return _embeddings

    import os
    onnx_extracted_path = os.path.expanduser("~/.cache/chroma/onnx_models/all-MiniLM-L6-v2/model.onnx")
    if os.path.exists(onnx_extracted_path):
        try:
            from chromadb.utils import embedding_functions
            default_ef = embedding_functions.DefaultEmbeddingFunction()
            _embeddings = ChromaEmbeddingWrapper(default_ef)
            logger.info("ChromaDB ONNX embedding function loaded.")
            return _embeddings
        except Exception as e:
            logger.warning(f"Failed loading ONNX embeddings: {e}")

    # Use fast 384-dim semantic hash embeddings (zero download, instantaneous, offline)
    logger.info("Using FallbackHashEmbeddings (384-dim, unit-normalized, instant).")
    _embeddings = FallbackHashEmbeddings(dim=384)
    return _embeddings
