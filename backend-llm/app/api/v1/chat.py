# Framework for exposing the API with Python
from fastapi import APIRouter, HTTPException

# Ollama for HTTP calls to the Ollama daemon
import ollama

from app.core.settings import settings  # to load the model name
from app.schemas.chat import (
    ChatRequest,
    ChatResponse,
)  # to manage the defined schemes along with their responses.

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
def chat(req: ChatRequest):
    try:
        res = ollama.chat(
            model=settings.MODEL_NAME,
            messages=[{"role": "user", "content": req.prompt}],
            stream=False,
        )
        return {"response": res["message"]["content"]}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
