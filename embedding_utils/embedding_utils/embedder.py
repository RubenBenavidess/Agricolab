# embedding_utils/embedder.py
import os
from pathlib import Path
from langchain_huggingface import HuggingFaceEmbeddings


def _make_embedder() -> HuggingFaceEmbeddings:
    """
    Crea una instancia de HuggingFaceEmbeddings leyendo las variables de entorno
    EMBED_MODEL y EMBED_CACHE_FOLDER (o usa ~/.cache/hf si no existe).
    """
    model_name = os.getenv(
        "EMBED_MODEL",
        "sentence-transformers/all-MiniLM-L6-v2"
    )
    cache_folder = os.getenv(
        "EMBED_CACHE_FOLDER",
        str(Path.home() / ".cache" / "hf")
    )
    # Asegura que exista el directorio de caché
    Path(cache_folder).mkdir(parents=True, exist_ok=True)
    return HuggingFaceEmbeddings(
        model_name=model_name,
        cache_folder=cache_folder
    )


def get_embeddings(texts: list[str]) -> list[list[float]]:
    """
    Genera embeddings para una lista de textos usando LangChain/HuggingFaceEmbeddings.

    :param texts: Lista de cadenas a embeddizar.
    :return: Lista de vectores de embedding correspondientes.
    """
    embedder = _make_embedder()
    return embedder.embed_documents(texts)


def get_embedding(text: str) -> list[float]:
    """
    Genera el embedding de un solo texto.

    :param text: Cadena de texto a embeddizar.
    :return: Vector de embedding.
    """
    embedder = _make_embedder()
    return embedder.embed_query(text)
