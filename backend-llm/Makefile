run:        ## Init API
	uvicorn app.main:app --reload --port 8000

test:       ## Executes Pytest
	python -m pytest -q

lint:       ## Checks linter with Ruff
	ruff check .

freeze:     ## Updates requirements.txt
	pip freeze > requirements.txt
