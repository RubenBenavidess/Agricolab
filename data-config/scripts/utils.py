import os
from pathlib import Path

def env(key, default=None):
    """
    Retrieves an environment variable, returning a default value if not set.
    Raises RuntimeError if the variable is not set and no default is provided.
    """
    val = os.getenv(key, default)
    if val is None:
        raise RuntimeError(f"Missing env var {key}")
    return val

def ensure_dirs(*dirs):
    """
    Ensures that the specified directories exist, creating them if necessary.
    Accepts multiple directory paths as arguments.
    """
    for d in dirs:
        Path(d).mkdir(parents=True, exist_ok=True)