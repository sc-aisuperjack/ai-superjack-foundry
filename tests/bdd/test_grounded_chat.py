from pytest_bdd import given, parsers, scenarios, then, when
from fastapi.testclient import TestClient
import pytest

from apps.api_gateway.main import app

scenarios("../fixtures/grounded_chat.feature")
client = TestClient(app)


@pytest.fixture
def scenario_context() -> dict:
    return {}


@given(parsers.parse('a stored document titled "{title}" with content "{content}"'))
def stored_document(title: str, content: str) -> None:
    client.post(
        "/v1/documents/upload",
        json={"title": title, "content": content, "metadata": {"source": "bdd"}},
    )


@when(parsers.parse('the user asks "{query}"'))
def ask_query(query: str, scenario_context: dict) -> None:
    response = client.post(
        "/v1/chat/query",
        json={"query": query, "provider": "mock", "mode": "text"},
    )
    scenario_context["response"] = response


@then("the answer should contain grounded content")
def answer_contains_grounding(scenario_context: dict) -> None:
    assert scenario_context["response"].status_code == 200
    assert "Grounded answer" in scenario_context["response"].json()["answer"]
