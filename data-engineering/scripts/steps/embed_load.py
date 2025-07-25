import os, json, glob
import chromadb
from langchain_community.embeddings import HuggingFaceEmbeddings
from scripts.utils import env, ensure_dirs

def embed_all():
    CHUNK_DIR   = env("CHUNK_DIR")
    CHROMA_PATH = env("CHROMA_PATH")
    MODEL_NAME  = env("EMBED_MODEL", "BAAI/bge-m3")

    ensure_dirs(CHROMA_PATH)

    client = chromadb.PersistentClient(path=CHROMA_PATH)
    collection = client.get_or_create_collection(name="agro_docs", metadata={"hnsw:space":"cosine"})
    embedder = HuggingFaceEmbeddings(model_name=MODEL_NAME)

    for path in glob.glob(os.path.join(CHUNK_DIR, "*.jsonl")):
        print("Embedding:", path)
        docs, metas, ids = [], [], []
        with open(path, encoding="utf-8") as f:
            for line in f:
                item = json.loads(line)
                docs.append(item["text"])
                metas.append({k:v for k,v in item.items() if k != "text"})
                ids.append(item["chunk_id"])

        vectors = embedder.embed_documents(docs)
        collection.add(ids=ids, documents=docs, metadatas=metas, embeddings=vectors)

    print("Total chunks:", collection.count())
