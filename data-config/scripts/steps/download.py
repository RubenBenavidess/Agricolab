"""
steps/download.py   –   descarga PDF/CSV/XLSX listados indirectamente.

Cambios clave
-------------
1. safe_str()       – convierte NaN en "".
2. links_from_sitemap() lee sitemaps .xml o .gz.
3. find_links()     – mismo dominio, filtra tel:/mailto:, profundidad.
4. is_file()        – detecta .pdf|.csv|.xlsx antes de ?, #, etc.
5. FILTRO KW        – si el set filtrado por keywords queda vacío,
                        se conserva el set original (evita “0 archivos”).
"""

import os, re, math, gzip, requests, xml.etree.ElementTree as ET
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from tqdm import tqdm
import pandas as pd

from scripts.utils import env, ensure_dirs

# ------------------------------------------------------------------ #
# utilidades
# ------------------------------------------------------------------ #
def safe_str(val) -> str:
    return "" if (isinstance(val, float) and math.isnan(val)) else str(val).strip()


def same_domain(a: str, b: str) -> bool:
    return urlparse(a).netloc.split(":")[0].lower() == urlparse(b).netloc.split(":")[0].lower()


def is_file(u: str, exts: tuple[str, ...]) -> bool:
    u_low = u.lower()
    return any(re.search(rf"\.{e}(\?|#|$)", u_low) for e in exts)


SKIP_SCHEMES = ("mailto:", "tel:", "javascript:", "#")


# ------------------------------------------------------------------ #
# sitemap
# ------------------------------------------------------------------ #
def links_from_sitemap(url: str, exts=("pdf",)) -> set[str]:
    try:
        r = requests.get(url, timeout=30, headers={"User-Agent": "Mozilla/5.0"})
        r.raise_for_status()
        xml_bytes = gzip.decompress(r.content) if url.endswith(".gz") else r.content
        root = ET.fromstring(xml_bytes)
        locs = [loc.text for loc in root.iter("{*}loc")]
        return {l for l in locs if is_file(l, exts)}
    except Exception as e:
        print("[WARN sitemap]", url, e)
        return set()


# ------------------------------------------------------------------ #
# crawler superficial
# ------------------------------------------------------------------ #
def find_links(base_url: str, extensions=("pdf",), depth=2, visited=None) -> set[str]:
    visited = visited or set()
    if base_url in visited:
        return set()
    visited.add(base_url)

    try:
        r = requests.get(base_url, headers={"User-Agent": "Mozilla/5.0"}, timeout=25)
        r.raise_for_status()
    except Exception as e:
        print(f"[WARN] {base_url}: {e}")
        return set()

    soup = BeautifulSoup(r.text, "html.parser")
    hrefs = {urljoin(base_url, a["href"]) for a in soup.find_all("a", href=True)}

    files = {u for u in hrefs if is_file(u, extensions) and
        not any(u.lower().startswith(s) for s in SKIP_SCHEMES)}

    if depth > 1:
        for link in list(hrefs)[:20]:
            if same_domain(base_url, link):
                files |= find_links(link, extensions, depth - 1, visited)

    return files


# ------------------------------------------------------------------ #
# paso principal
# ------------------------------------------------------------------ #
def download_all():
    SHEET_CSV_URL = env("SHEET_CSV_URL")
    RAW_DIR = env("RAW_DIR")
    ensure_dirs(RAW_DIR)

    df = pd.read_csv(SHEET_CSV_URL)
    all_links: set[str] = set()

    for _, row in df.iterrows():
        base_url = safe_str(row.get("Base URL"))
        if not base_url:
            continue

        # extensiones
        filetypes = [t.strip().lower()
            for t in safe_str(row.get("Filetypes to grab (pdf,csv,xlsx)", "pdf")).split(",")]
        exts = tuple(e for e in ("pdf", "csv", "xlsx") if e in filetypes)

        # palabras clave
        kws = [k.strip() for k in safe_str(row.get("Spanish Keywords")).split(",") if k.strip()]
        regex = re.compile("|".join(map(re.escape, kws)), re.IGNORECASE) if kws else None

        depth = int(row.get("Crawl Depth (levels)", 1) or 1)
        sitemap = safe_str(row.get("Sitemap URL"))

        links = links_from_sitemap(sitemap, exts) if sitemap else \
                find_links(base_url, extensions=exts, depth=depth)

        if regex:
            filtered = {u for u in links if regex.search(u.lower())}
            if filtered:   # solo aplica si hay coincidencias
                links = filtered

        all_links |= links

    print(f"[DOWNLOAD] se encontraron {len(all_links)} archivos")

    for url in tqdm(sorted(all_links), desc="Downloading"):
        fname = url.split("/")[-1].split("?")[0]
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
