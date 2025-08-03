# embedding_utils/embedder.py
import os
from langchain_huggingface import HuggingFaceEmbeddings

# Lee la configuración del modelo de embeddings desde variables de entorno
MODEL_NAME = os.getenv("EMBED_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
CACHE_FOLDER = os.getenv("EMBED_CACHE_FOLDER", "/app/.hf")

# Instancia global del embedder de LangChain/HuggingFace
_embedder = HuggingFaceEmbeddings(
    model_name=MODEL_NAME,
    cache_folder=CACHE_FOLDER
)

def get_embeddings(texts: list[str]) -> list[list[float]]:
    """
    Genera embeddings para una lista de textos usando el modelo configurado.

    :param texts: Lista de cadenas a embeddizar.
    :return: Lista de vectores de embedding correspondientes.
    """
    # embed_documents devuelve una lista de vectores (uno por texto)
    return _embedder.embed_documents(texts)

def get_embedding(text: str) -> list[float]:
    """
    Genera el embedding de un solo texto.

    :param text: Cadena de texto a embeddizar.
    :return: Vector de embedding.
    """
    return _embedder.embed_query(text)