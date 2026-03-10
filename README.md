# Agentic Foundry

A production-style boilerplate for building grounded, voice-enabled, agentic AI applications with Streamlit, FastAPI, LangGraph, MCP, MongoDB Atlas, Redis, and multi-LLM support.

## What this is

This repository is a senior-style scaffold for an AI operations copilot. It includes:

- Streamlit demo UI
- FastAPI gateway
- LangGraph-inspired orchestration graph
- MCP server scaffold
- MongoDB repositories and vector-ready document models
- Redis-backed cache and session memory
- Speech service interfaces for STT and TTS
- Multi-provider LLM abstraction
- Celery worker scaffold
- Unit, integration, and BDD test structure
- Docker Compose for local development

## Current status

This is a **scaffolded boilerplate**. It is designed to run locally and provide a strong structure, sample flows, and working endpoints. Some integrations are deliberately lightweight or mocked by default so the project is easy to start and extend.

## Architecture

```text
Streamlit UI
    -> FastAPI Gateway
        -> Orchestration Service
            -> Retrieval Service
            -> LLM Router
            -> MCP Client
            -> Redis Cache
            -> MongoDB Repository
            -> Speech Service
```

## Quick start

### 1. Copy environment file

```bash
cp .env.example .env
```

### 2. Start infrastructure

```bash
docker compose up -d mongodb redis
```

### 3. Install dependencies

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

### 4. Run the API

```bash
uvicorn apps.api_gateway.main:app --reload --port 8000
```

### 5. Run the Streamlit app

```bash
streamlit run apps/streamlit_app/app.py
```

## Core features scaffolded

### API
- `GET /health`
- `POST /v1/chat/query`
- `POST /v1/documents/upload`
- `GET /v1/traces/{trace_id}`

### UI
- Text and voice-style input areas
- Demo upload screen
- Trace and citation rendering

### Orchestration
- Input classification
- Retrieval-first workflow
- Optional tool path placeholder
- Grounded answer assembly

### Tests
- Unit tests for chunking and cache keys
- Integration-style API tests
- BDD feature examples

## Suggested next steps

1. Wire real embedding and vector indexing into MongoDB Atlas.
2. Upgrade the graph to full LangGraph nodes and persistence.
3. Connect OpenAI or Anthropic providers with environment keys.
4. Replace demo speech adapters with real STT and TTS calls.
5. Add background ingestion with Celery.
6. Add observability via OpenTelemetry or Langfuse.

## Repo layout

```text
apps/
  streamlit_app/
  api_gateway/
  worker/
  mcp_server/
services/
  orchestration/
  retrieval/
  llm_router/
  speech/
  memory/
  data/
  evals/
  observability/
shared/
  contracts/
  config/
  utils/
  prompts/
tests/
docs/
```

## License

MIT
