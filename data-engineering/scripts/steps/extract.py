import os, json, re
import pdfplumber
from scripts.utils import env, ensure_dirs

def extract_text(pdf_path):
    pages = []
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            raw = page.extract_text() or ""
            pages.append({"page": i+1, "text": raw})
    return pages

def extract_all():
    RAW_DIR = env("RAW_DIR")
    INTERIM_DIR = env("INTERIM_DIR")
    ensure_dirs(INTERIM_DIR)

    for fname in os.listdir(RAW_DIR):
        if not fname.lower().endswith(".pdf"):
            continue
        src = os.path.join(RAW_DIR, fname)
        out = os.path.join(INTERIM_DIR, fname.replace(".pdf", "_text.json"))
        if os.path.exists(out):
            continue
        print("Extract:", fname)
        pages = extract_text(src)
        with open(out, "w", encoding="utf-8") as f:
            json.dump(pages, f, ensure_ascii=False, indent=2)
