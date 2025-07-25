import os, json, uuid
from scripts.utils import env, ensure_dirs

CHUNK_SIZE = 600  # tokens aproximados → aquí usamos palabras

def chunk_text(text, chunk_size=CHUNK_SIZE, overlap=80):
    words = text.split()
    start = 0
    chunks = []
    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start = end - overlap
        if start < 0: start = 0
    return chunks

def chunk_all():
    CLEAN_DIR = env("CLEAN_DIR")
    CHUNK_DIR = env("CHUNK_DIR")
    ensure_dirs(CHUNK_DIR)

    for fname in os.listdir(CLEAN_DIR):
        if not fname.endswith("_clean.json"):
            continue
        doc_id = fname.replace("_clean.json", "")
        with open(os.path.join(CLEAN_DIR, fname), encoding="utf-8") as f:
            pages = json.load(f)

        all_chunks = []
        for p in pages:
            for c in chunk_text(p["text"]):
                if len(c.split()) < 50:
                    continue
                all_chunks.append({
                    "doc_id": doc_id,
                    "chunk_id": f"{doc_id}_{uuid.uuid4().hex[:8]}",
                    "text": c,
                    # metadata mínima; luego puedes enriquecer
                    "pages": str(p["page"])
                })

        out = os.path.join(CHUNK_DIR, doc_id + ".jsonl")
        with open(out, "w", encoding="utf-8") as f:
            for item in all_chunks:
                f.write(json.dumps(item, ensure_ascii=False) + "\n")
