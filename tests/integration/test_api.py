from fastapi.testclient import TestClient

from apps.api_gateway.main import app

client = TestClient(app)


def test_health_endpoint() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_upload_and_query() -> None:
    upload = client.post(
        "/v1/documents/upload",
        json={
            "title": "Platform Overview",
            "content": "Agentic Foundry uses FastAPI, Streamlit, MongoDB, Redis, MCP, and orchestration.",
            "metadata": {"source": "test"},
        },
    )
    assert upload.status_code == 200

    query = client.post(
        "/v1/chat/query",
        json={
            "query": "What does Agentic Foundry use?",
            "provider": "mock",
            "mode": "text",
        },
    )
    assert query.status_code == 200
    payload = query.json()
    assert "answer" in payload
    assert len(payload["citations"]) >= 1
