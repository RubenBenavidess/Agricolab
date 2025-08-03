import os
import pytest
from embedding_utils import get_embeddings, get_embedding

@pytest.fixture(autouse=True)
def set_env(monkeypatch):
    # Fuerza un modelo pequeño para tests rápidos
    monkeypatch.setenv("EMBED_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
    monkeypatch.setenv("EMBED_CACHE_FOLDER", "./tmp/.hf")

def test_get_embedding_shape():
    vec = get_embedding("Hola mundo")
    assert isinstance(vec, list)
    assert len(vec) > 0

def test_get_embeddings_shape():
    texts = ["uno", "dos", "tres"]
    vecs = get_embeddings(texts)
    assert isinstance(vecs, list) and len(vecs) == 3
    assert all(isinstance(v, list) for v in vecs)
