from fakes import ScriptedToolCallingChatModel
from fastapi.testclient import TestClient
from langchain_core.messages import AIMessage

from foodagent.api import app, get_model, get_sessions, get_settings
from foodagent.config import Settings
from foodagent.sessions import SessionStore


def _client_with_fake_model(responses: list) -> TestClient:
    app.dependency_overrides[get_model] = lambda: ScriptedToolCallingChatModel(responses=responses)
    app.dependency_overrides[get_settings] = lambda: Settings(_env_file=None)
    app.dependency_overrides[get_sessions] = lambda: SessionStore()
    return TestClient(app)


def test_health_returns_ok():
    client = _client_with_fake_model([])
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_chat_endpoint_returns_reply_and_cart():
    responses = [
        AIMessage(
            content="",
            tool_calls=[
                {
                    "name": "adicionar_ao_carrinho",
                    "args": {"item_id": "pizza-margherita", "quantidade": 1},
                    "id": "1",
                },
            ],
        ),
        AIMessage(content="Pizza adicionada ao carrinho."),
    ]
    client = _client_with_fake_model(responses)

    response = client.post("/chat", json={"session_id": "s1", "message": "quero uma pizza"})

    assert response.status_code == 200
    body = response.json()
    assert "reply" in body
    assert len(body["carrinho"]) == 1
    assert body["subtotal"] > 0
