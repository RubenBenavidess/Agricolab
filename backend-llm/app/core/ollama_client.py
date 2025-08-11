# app/core/ollama_client.py
from functools import lru_cache
from ollama import Client
from app.core.settings import settings

@lru_cache(maxsize=1)
def get_ollama_client() -> Client:
    return Client(host=settings.OLLAMA_HOST)