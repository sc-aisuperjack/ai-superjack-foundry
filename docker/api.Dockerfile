FROM python:3.11-slim
WORKDIR /app
COPY pyproject.toml README.md ./
COPY apps ./apps
COPY services ./services
COPY shared ./shared
RUN pip install --no-cache-dir -e .
CMD ["uvicorn", "apps.api_gateway.main:app", "--host", "0.0.0.0", "--port", "8000"]
