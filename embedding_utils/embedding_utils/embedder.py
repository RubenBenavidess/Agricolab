# embedding_utils/embedder.py
import os
from pathlib import Path
from langchain_huggingface import HuggingFaceEmbeddings


def _make_embedder() -> HuggingFaceEmbeddings:
    """
    Creates and returns an instance of HuggingFaceEmbeddings using environment variables for configuration.
    If the cache folder does not exist, it will be created automatically.
    Returns:
        HuggingFaceEmbeddings: An initialized HuggingFaceEmbeddings object with the specified model and cache folder.
    """
    model_name = os.getenv(
        "EMBED_MODEL",
        "BAAI/bge-m3"
    )
    cache_folder = os.getenv(
        "EMBED_CACHE_FOLDER",
        str(Path.home() / ".cache" / "hf")
    )

    Path(cache_folder).mkdir(parents=True, exist_ok=True)
    return HuggingFaceEmbeddings(
        model_name=model_name,
        cache_folder=cache_folder
    )


def get_embeddings(texts: list[str]) -> list[list[float]]:
    """
    Generates embeddings for a list of texts using LangChain/HuggingFaceEmbeddings.
    Args:
        texts (list[str]): List of strings to generate embeddings for.
    Returns:
        list[list[float]]: List of embedding vectors corresponding to the input texts.
    """
    embedder = _make_embedder()
    return embedder.embed_documents(texts)


def get_embedding(text: str) -> list[float]:
    """
    Generates embeddings for single text using LangChain/HuggingFaceEmbeddings.
    Args:
        texts (str): String to generate embeddings for.
    Returns:
        list[list[float]]: List of embedding vectors corresponding to the input text
    """
    embedder = _make_embedder()
    return embedder.embed_query(text)
