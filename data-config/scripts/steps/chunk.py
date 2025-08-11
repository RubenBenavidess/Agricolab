import os
import json
import uuid
import shutil

from scripts.utils import env, ensure_dirs

CHUNK_SIZE = 600
OVERLAP    = 80 

def chunk_text(text: str, chunk_size=CHUNK_SIZE, overlap=OVERLAP):
    """
    Splits text into overlapping chunks.
    """
    words = text.split()
    n = len(words)
    if n == 0:
        return
    
    if n <= chunk_size:
        yield " ".join(words)
        return
    
    start = 0
    while start < n:
        end = min(start + chunk_size, n)
        yield " ".join(words[start:end])

        if end == n:
            break

        start = end - overlap

        if start < 0:
            start = 0

def chunk_all():
    """
    Processes all *_clean.json files in CLEAN_DIR, chunks the text,
    and saves to CHUNK_DIR as *_chunk.jsonl.
    Each chunk is a JSONL record with doc_id, chunk_id, text, and pages.
    """
    
    CLEAN_DIR = env("CLEAN_DIR")
    CHUNK_DIR = env("CHUNK_DIR")

    if os.path.isdir(CHUNK_DIR):
        shutil.rmtree(CHUNK_DIR)
    ensure_dirs(CHUNK_DIR)

    files = [f for f in os.listdir(CLEAN_DIR) if f.endswith("_clean.json")]
    print(f"[DEBUG] {len(files)} documents in {CLEAN_DIR}: {files}")

    for fname in files:
        doc_id = fname.replace("_clean.json", "")
        in_path  = os.path.join(CLEAN_DIR, fname)
        out_path = os.path.join(CHUNK_DIR, f"{doc_id}.jsonl")

        written = 0
        print(f"[DEBUG] Chunking {fname} → {out_path}")

        with open(in_path, encoding="utf-8") as fin, \
             open(out_path, "w", encoding="utf-8") as fout:

            try:
                pages = json.load(fin)
            except json.JSONDecodeError as e:
                print(f"[ERROR] Malformed JSON in {in_path}: {e}")
                continue

            for p in pages:
                text = p.get("text", "")
                for chunk in chunk_text(text):
                    # discard very short fragments
                    if len(chunk.split()) < 50:
                        continue
                    record = {
                        "doc_id":   doc_id,
                        "chunk_id": f"{doc_id}_{uuid.uuid4().hex[:8]}",
                        "text":     chunk,
                        "pages":    str(p.get("page", ""))
                    }
                    fout.write(json.dumps(record, ensure_ascii=False) + "\n")
                    written += 1

        print(f"[CHUNK] {fname}: wrote {written} chunks")

    print(f"[CHUNK] END: {len(os.listdir(CHUNK_DIR))} documents with generated chunks.")

