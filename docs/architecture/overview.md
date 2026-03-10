# Architecture Overview

Agentic Foundry is designed as a modular AI application scaffold.

## Layers

1. Presentation layer via Streamlit
2. API layer via FastAPI
3. Orchestration layer via agent graph service
4. Retrieval layer for chunking and grounded lookup
5. Data layer via MongoDB and Redis
6. Integration layer for MCP, LLM providers, and speech

## Why this shape

This structure keeps the demo believable and extensible. It separates the interface from the orchestration logic so the same backend can later serve a web app, CLI, or Slack bot.
