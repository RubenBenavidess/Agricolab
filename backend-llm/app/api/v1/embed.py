# Framework for exposing the API with Python
from fastapi import APIRouter, HTTPException

# Ollama for HTTP calls to the Ollama daemon
import ollama

from app.core.settings import settings  # to load the model name
from app.schemas.embed import (
    EmbedRequest,
    EmbedResponse,
)  # to manage the defined schemes along with their responses.

router = APIRouter(prefix="/embed", tags=["embed"])


@router.post("", response_model=EmbedResponse)
def create_embed(req: EmbedRequest) -> EmbedResponse:
    if not req.text.strip():
        raise HTTPException(status_code=422, detail="Field text empty.")
    try:
        res = ollama.embeddings(model=settings.EMBED_MODEL_NAME, prompt=req.text)
        return {"embedding": res["embedding"]}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
