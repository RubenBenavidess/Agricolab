from fastapi import APIRouter, HTTPException
import ollama

from app.core.settings import settings
from app.schemes.rag_model import RagRequest, RagResponse
from app.schemes.chat_model import ChatRequest
from embedding_utils.embedder import get_embedding
from app.api.services.vectorstore import get_top_k_chunks
from .chat import chat

router = APIRouter(prefix="/agricolab/api", tags=["rag"])


@router.post("", response_model=RagResponse)
def rag(req: RagRequest) -> RagResponse:
    question = req.question
    n_docs = req.n_docs

    # 1. Embedding de la pregunta
    try:
        question_embedding = get_embedding(question)
    except Exception as exc:
        raise HTTPException(500, f"Error en la generación de vectores: {exc}")

    # 2. Recuperar documentos
    try:
        chunks = get_top_k_chunks(question_embedding, k=n_docs)
    except Exception as exc:
        raise HTTPException(500, f"Error en vector store: {exc}")

    # 3. Construir contexto
    context_blocks = []
    for c in chunks:
        source = c.metadata.get("source", c.metadata.get("chunk_id", "desconocido"))
        context_blocks.append(f"Fuente: {source}\nTexto: {c.text}")
    context = "\n\n".join(context_blocks)

    full_prompt = (
        "Usa el siguiente contexto para responder de forma concisa si aplica a la pregunta:\n\n"
        f"{context}\n\n"
        f"Pregunta: {question}\n"
        "Respuesta:"
    )

    # 4. Llamar al modelo chat
    answer = chat(ChatRequest(prompt=full_prompt))["response"]

    # 5. Devolver respuesta y fuentes
    sources = [c.metadata.get("source", "") for c in chunks]
    return RagResponse(answer=answer, sources=sources)
