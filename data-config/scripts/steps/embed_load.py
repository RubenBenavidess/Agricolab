import os
import json
import glob
import uuid

import chromadb
from scripts.utils import env, ensure_dirs
from embedding_utils.embedder import get_embeddings

def embed_all():
    """
    Reads JSONL files from CHUNK_DIR, generates embeddings, and adds them to the ChromaDB collection.
    """
    CHUNK_DIR   = env("CHUNK_DIR")
    CHROMA_PATH = env("CHROMA_PATH")

    ensure_dirs(CHROMA_PATH)

    client = chromadb.PersistentClient(path=CHROMA_PATH)
    collection = client.get_or_create_collection(
        name="agro_docs",
        metadata={"hnsw:space": "cosine"}
    )

    paths = sorted(glob.glob(os.path.join(CHUNK_DIR, "*.jsonl")))
    print(f"[DEBUG] Files to embed ({len(paths)}): {paths}")

    for path in paths:
        print(f"[DEBUG] Embedding: {path}")
        docs, metas, ids = [], [], []

        with open(path, encoding="utf-8") as f:
            for line in f:
                try:
                    item = json.loads(line)
                except json.JSONDecodeError as e:
                    print(f"[WARNING] Malformed JSON in {path}: {e}")
                    continue

                text    = item.get("text", "").strip()
                chunk_id = item.get("chunk_id") or str(uuid.uuid4())
                if not text:
                    continue

                docs.append(text)
                metas.append({k:v for k,v in item.items() if k not in ("text",)})
                ids.append(chunk_id)

        if not docs:
            print(f"[WARNING] No chunks found in {path}, skipping.")
            continue

        try:
            vectors = get_embeddings(docs)
        except Exception as e:
            print(f"[ERROR] embed_documents failed for {path}: {e}")
            continue

        if not vectors:
            print(f"[WARNING] embedder returned 0 vectors for {path}, skipping.")
            continue

        try:
            collection.add(
                ids=ids,
                documents=docs,
                metadatas=metas,
                embeddings=vectors
            )
        except Exception as e:
            print(f"[ERROR] collection.add failed for {path}: {e}")
            continue

    total = collection.count()
    print(f"[EMBED] Total chunks in collection: {total}")
