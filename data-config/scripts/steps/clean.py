import os, json, unicodedata, re
from scripts.utils import env, ensure_dirs

def normalize_units(txt):
    """
    Normalizes agricultural units in the text.
    """
    return txt.replace(" Kg/Ha", " kg/ha").replace("Kg/Ha", " kg/ha")

def clean_all():
    """
    Processes all *_text.json files in INTERIM_DIR, cleans the text,
    and saves to CLEAN_DIR as *_clean.json.
    Cleans includes:
    - Normalizing unicode
    - Removing extra whitespace
    - Removing hyphenated line breaks
    - Normalizing agricultural units
    """
    INTERIM_DIR = env("INTERIM_DIR")
    CLEAN_DIR = env("CLEAN_DIR")
    ensure_dirs(CLEAN_DIR)

    for fname in os.listdir(INTERIM_DIR):
        if not fname.endswith("_text.json"):
            continue
        with open(os.path.join(INTERIM_DIR, fname), encoding="utf-8") as f:
            pages = json.load(f)

        cleaned = []
        for p in pages:
            t = unicodedata.normalize("NFKC", p["text"])
            t = re.sub(r'\s+', ' ', t)
            t = re.sub(r'-\s+', '', t)
            t = normalize_units(t)
            cleaned.append({"page": p["page"], "text": t.strip()})

        out = os.path.join(CLEAN_DIR, fname.replace("_text.json", "_clean.json"))
        with open(out, "w", encoding="utf-8") as f:
            json.dump(cleaned, f, ensure_ascii=False, indent=2)
