install:
	pip install -e .[dev]

run-api:
	uvicorn apps.api_gateway.main:app --reload --port 8000

run-ui:
	streamlit run apps/streamlit_app/app.py

test:
	pytest

lint:
	ruff check .
