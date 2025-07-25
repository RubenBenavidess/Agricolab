# Agricolab LLM API

# Requirements
- Ollama with gemma3:4b
- Python 3.11+
- Pip

# IMPORTANT: Init the environment (ONLY EXECUTE THE FIRST TIME)
python -m venv .venv
## OR WINDOWS
python -m venv .venv
PowerShell: .\.venv\Scripts\Activate.ps1
CMD: .\.venv\Scripts\activate.bat 

# Update the environment
pip install -r requirements.txt

# IMPORTANT (ONLY EXECUTE THE FIRST TIME): Run pre-commits
pip install pre-commit

# IMPORTANT TO RUN API: LOAD environment
source .venv/bin/activate

# Init API
make run
## OR WINDOWS
uvicorn app.main:app --reload --port 8000

# Test
make test
## OR WINDOWS
python -m pytest -q
