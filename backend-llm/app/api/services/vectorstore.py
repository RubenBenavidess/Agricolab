import os
from typing import List, NamedTuple, Optional, Dict, Any
from chromadb import HttpClient
from chromadb.config import Settings as ChromaSettings
from embedding_utils.embedder import get_embeddings

COLLECTION_NAME = "agro_docs"
HNSW_META = {"hnsw:space": "cosine"}

class Chunk(NamedTuple):
    id: str
    text: str
    metadata: dict
    distance: float
    similarity: float

def _build_client() -> HttpClient:
    host = os.getenv("CHROMA_SERVER_HOST", "chroma")
    port = int(os.getenv("CHROMA_SERVER_HTTP_PORT", 8000))
    settings = ChromaSettings(
        chroma_api_impl="chromadb.api.fastapi.FastAPI",
        anonymized_telemetry=False,
    )
    return HttpClient(host=host, port=port, settings=settings)

client = _build_client()

collection = client.get_or_create_collection(
    name=COLLECTION_NAME,
    metadata=HNSW_META
)

def _to_chunks(result: Dict[str, Any]) -> List[Chunk]:
    ids        = result["ids"][0]
    docs       = result.get("documents", [[]])[0]
    metas      = result.get("metadatas", [[]])[0]
    distances  = result.get("distances", [[]])[0]
    out: List[Chunk] = []
    for i, d, m, dist in zip(ids, docs, metas, distances):
        sim = 1.0 - dist if dist is not None else float("nan")
        out.append(Chunk(id=i, text=d, metadata=m or {}, distance=dist, similarity=sim))
    return out

def get_top_k_chunks(
    embedding: List[float],
    k: int = 4,
    where: Optional[Dict[str, Any]] = None,
) -> List[Chunk]:
    res = collection.query(
        query_embeddings=[embedding],
        n_results=k,
        include=["documents", "metadatas", "distances"],
        where=where or {}
    )
    return _to_chunks(res)

def get_top_k_chunks_by_text(
    query: str,
    k: int = 4,
    where: Optional[Dict[str, Any]] = None,
) -> List[Chunk]:
    vec = get_embeddings([query])[0]
    return get_top_k_chunks(vec, k=k, where=where)
