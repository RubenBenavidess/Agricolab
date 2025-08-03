import os
import json
import glob
import uuid

import chromadb
from scripts.utils import env, ensure_dirs
from embedding_utils.embedder import get_embeddings

def embed_all():
    """
    Por cada .jsonl en CHUNK_DIR, extrae los textos, genera embeddings en lotes
    y los añade a ChromaDB. Se saltan archivos vacíos o con errores.
    """
    CHUNK_DIR   = env("CHUNK_DIR")
    CHROMA_PATH = env("CHROMA_PATH")

    # Asegura que exista la carpeta de persistencia de ChromaDB
    ensure_dirs(CHROMA_PATH)

    # Conecta/crea la colección
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    collection = client.get_or_create_collection(
        name="agro_docs",
        metadata={"hnsw:space": "cosine"}
    )

    # Lista y recorre cada archivo JSONL de chunks
    paths = sorted(glob.glob(os.path.join(CHUNK_DIR, "*.jsonl")))
    print(f"[DEBUG] Archivos a embedear ({len(paths)}): {paths}")

    for path in paths:
        print(f"[DEBUG] Embedding: {path}")
        docs, metas, ids = [], [], []

        # Lee cada línea (cada chunk)
        with open(path, encoding="utf-8") as f:
            for line in f:
                try:
                    item = json.loads(line)
                except json.JSONDecodeError as e:
                    print(f"[WARNING] JSON mal formado en {path}: {e}")
                    continue

                text    = item.get("text", "").strip()
                chunk_id = item.get("chunk_id") or str(uuid.uuid4())
                if not text:
                    continue

                docs.append(text)
                metas.append({k:v for k,v in item.items() if k not in ("text",)})
                ids.append(chunk_id)

        # Si no hay docs, saltamos este archivo
        if not docs:
            print(f"[WARNING] No hay chunks en {path}, saltando.")
            continue

        # Genera embeddings y maneja posibles errores
        try:
            vectors = get_embeddings(docs)
        except Exception as e:
            print(f"[ERROR] Falló embed_documents en {path}: {e}")
            continue

        if not vectors:
            print(f"[WARNING] embedder devolvió 0 vectores para {path}, saltando.")
            continue

        # Añade a la colección, capturando errores para no detener todo
        try:
            collection.add(
                ids=ids,
                documents=docs,
                metadatas=metas,
                embeddings=vectors
            )
        except Exception as e:
            print(f"[ERROR] Falló collection.add para {path}: {e}")
            continue

    total = collection.count()
    print(f"[EMBED] Total de chunks en la colección: {total}")
