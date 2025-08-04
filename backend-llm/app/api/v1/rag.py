# Framework for exposing the API with Python
from fastapi import APIRouter, HTTPException

# Ollama for HTTP calls to the Ollama daemon
import ollama

# To load the model names
from app.core.settings import settings  

# To manage the defined schemes along with their responses.
from app.schemes.rag_model import (
    RagRequest,
    RagResponse
)
from embedding_utils.embedder import get_embedding
from app.schemes.chat_model import (
    ChatRequest,
    ChatResponse,
)

# To import defined functions for chatting and embedding
from .chat import chat

# Expose router
router = APIRouter(prefix='/agricolab/api', tags=['rag'])

@router.post("", response_model=RagResponse)
def rag(req: RagRequest) -> RagResponse:

    question = req.question
    n_docs = req.n_docs

    # Create embedding
    try:
        question_embedding = get_embedding(question)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Error en la generación de vectores: {exc}")

    # Get documents from service
    try:
        chunks = [
            {
                "metadata": {
                    "source": "Anónimo"
                },
                "text": "Un sistema de información es un conjunto de programas que cumplen con un objetivo o buscan solucionar problemas." 
            }
        ]
        # chunks = get_top_k_chunks(query_embedding, k=req.k)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Error en vector store: {exc}")

    # Build context
    context_blocks = []
    for c in chunks:
        source = c["metadata"].get("source", c["metadata"].get("chunk_id", "desconocido"))
        context_blocks.append(f"Fuente: {source}\nTexto: {c['text']}")
    context = "\n\n".join(context_blocks)

    full_prompt = (
        "Usa el siguiente contexto para responder de forma concisa si aplica para la pregunta:\n\n"
        f"{context}\n\n"
        f"Pregunta: {question}\n"
        "Respuesta:"
    )

    # Call chat
    answer = chat(
        ChatRequest(prompt=full_prompt)
    )["response"]

    # Return
    sources = [c["metadata"].get("source", "") for c in chunks]
    return RagResponse(answer=answer, sources=sources)









