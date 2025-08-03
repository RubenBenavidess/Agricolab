# Framework for exposing the API with Python
from fastapi import APIRouter, HTTPException

# Ollama for HTTP calls to the Ollama daemon
import ollama

# To load the model name
from app.core.settings import settings  

# to manage the defined schemes along with their responses.
from app.schemes.chat_model import (
    ChatRequest,
    ChatResponse,
) 

def chat(chatRequest: ChatRequest):
    try:
        res = ollama.chat(
            model=settings.MODEL_NAME,
            messages=[{"role": "user", "content": chatRequest.prompt}],
            stream=False,
        )
        return {"response": res["message"]["content"]}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
