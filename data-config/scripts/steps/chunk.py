import os
import json
import uuid
import shutil

from scripts.utils import env, ensure_dirs

CHUNK_SIZE = 600  # palabras por chunk
OVERLAP    = 80   # solapamiento en palabras

def chunk_text(text: str, chunk_size=CHUNK_SIZE, overlap=OVERLAP):
    """
    Generador que parte `text` en fragmentos de hasta chunk_size palabras,
    con solapamiento overlap. Se asegura de no repetir infinitamente.
    """
    words = text.split()
    n = len(words)
    if n == 0:
        return
    # si el texto es más corto que un chunk, yields one and done
    if n <= chunk_size:
        yield " ".join(words)
        return

    start = 0
    while start < n:
        end = min(start + chunk_size, n)
        yield " ".join(words[start:end])
        # si ya llegamos al final, rompemos
        if end == n:
            break
        # avanzamos, respetando overlap
        start = end - overlap
        # (por seguridad, no bajamos de 0)
        if start < 0:
            start = 0

def chunk_all():
    """
    Procesa todos los *_clean.json en CLEAN_DIR y escribe
    un JSONL por documento en CHUNK_DIR, limpiando al inicio.
    """
    CLEAN_DIR = env("CLEAN_DIR")
    CHUNK_DIR = env("CHUNK_DIR")

    # ——— Limpio CHUNK_DIR de ejecuciones previas ———
    if os.path.isdir(CHUNK_DIR):
        shutil.rmtree(CHUNK_DIR)
    ensure_dirs(CHUNK_DIR)

    # ——— Debug: qué ficheros vamos a procesar ———
    files = [f for f in os.listdir(CLEAN_DIR) if f.endswith("_clean.json")]
    print(f"[DEBUG] {len(files)} documentos en {CLEAN_DIR}: {files}")

    # ——— Por cada documento, escribo streaming al .jsonl ———
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
                print(f"[ERROR] JSON mal formado en {in_path}: {e}")
                continue

            for p in pages:
                text = p.get("text", "")
                for chunk in chunk_text(text):
                    # descartamos fragmentos muy cortos
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

        print(f"[CHUNK] {fname}: escritos {written} chunks")

    print(f"[CHUNK] END: {len(os.listdir(CHUNK_DIR))} documentos con chunks generados.")
