# Agricolab LLM API

# Requirements
- Ollama
- Python 3.11+
- Pip

# IMPORTANT: Init the environment
python -m venv .venv && source .venv/bin/activate
# OR WINDOWS
python -m venv .venv
PowerShell: .\.venv\Scripts\Activate.ps1
CMD: .\.venv\Scripts\activate.bat 

# Update the environment
pip install -r requirements.txt

# IMPORTANT (ONLY EXECUTE THE FIRST TIME): Run pre-commits
pip install pre-commit

# Init API
make run
# OR WINDOWS
uvicorn app.main:app --reload --port 8000

# Test
make test
# OR WINDOWS
python -m pytest -q
