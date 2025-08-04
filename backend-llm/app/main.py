# Framework for exposing the API with Python
from fastapi import FastAPI

# os to read environment variables
import os

from app.core.settings import settings  # load environment variables
from app.api.v1 import health, rag # import routers

# Sets the ollama SDK to see OLLAMA_HOST
os.environ["OLLAMA_HOST"] = settings.OLLAMA_HOST

app = FastAPI(
    title="Agricolab LLM API",
    version="0.1.0",
    description="Endpoints para chat y embeddings con Gemma 3 sobre Ollama.",
)

# Configure routers
app.include_router(health.router)
app.include_router(rag.router)
