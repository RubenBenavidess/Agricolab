import pandas as pd
import re, os, requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from tqdm import tqdm
from scripts.utils import env, ensure_dirs

def find_links(base_url, extensions=("pdf",)):
    try:
        r = requests.get(base_url, timeout=15)
        r.raise_for_status()
    except Exception as e:
        print(f"[WARN] {base_url}: {e}")
        return set()
    soup = BeautifulSoup(r.text, "html.parser")
    urls = set()
    for a in soup.find_all("a", href=True):
        href = a["href"].lower()
        if any(href.endswith(f".{ext}") for ext in extensions):
            urls.add(urljoin(base_url, a["href"]))
    return urls

def download_all():
    SHEET_CSV_URL = env("SHEET_CSV_URL")
    RAW_DIR = env("RAW_DIR")
    ensure_dirs(RAW_DIR)

    df = pd.read_csv(SHEET_CSV_URL)

    pdf_links = set()
    for _, row in df.iterrows():
        base = str(row.get("Base URL", "")).strip()
        if not base:
            continue
        filetypes = str(row.get("Filetypes to grab (pdf,csv,xlsx)", "pdf")).split(",")
        filetypes = [t.strip().lower() for t in filetypes]
        exts = [ext for ext in ["pdf","csv","xlsx"] if ext in filetypes]

        kws = str(row.get("Spanish Keywords", "")).split(",")
        kws = [k.strip() for k in kws if k.strip()]
        regex = re.compile("|".join(map(re.escape, kws)), re.IGNORECASE) if kws else None

        links = find_links(base, extensions=exts)
        if regex:
            links = {u for u in links if regex.search(u)}
        pdf_links |= links

    for url in tqdm(sorted(pdf_links), desc="Downloading"):
        fname = url.split("/")[-1]
        path = os.path.join(RAW_DIR, fname)
        if os.path.exists(path):
            continue
        try:
            with requests.get(url, stream=True, timeout=25) as r:
                r.raise_for_status()
                with open(path, "wb") as f:
                    for chunk in r.iter_content(8192):
                        f.write(chunk)
        except Exception as e:
            print(f"[ERROR] {url}: {e}")
