import os
from pathlib import Path

def env(key, default=None):
    val = os.getenv(key, default)
    if val is None:
        raise RuntimeError(f"Missing env var {key}")
    return val

def ensure_dirs(*dirs):
    for d in dirs:
        Path(d).mkdir(parents=True, exist_ok=True)