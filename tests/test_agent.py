from fakes import ScriptedToolCallingChatModel
from langchain_core.messages import AIMessage

from foodagent.agent import chat
from foodagent.config import Settings
from foodagent.sessions import Session


def test_chat_resolves_tool_call_and_returns_final_reply():
    responses = [
        AIMessage(
            content="",
            tool_calls=[
                {"name": "buscar_cardapio", "args": {"query": "pizza"}, "id": "1"},
            ],
        ),
        AIMessage(content="Temos pizza margherita, quatro queijos e pepperoni."),
    ]
    model = ScriptedToolCallingChatModel(responses=responses)
    session = Session()
    settings = Settings(_env_file=None)

    reply = chat(model, session, "quais pizzas vocês têm?", settings)

    assert "pizza" in reply.lower()
    assert len(session.history) == 4  # human, ai+tool_call, tool, ai final


def test_chat_persists_cart_state_across_turns():
    responses_turn_1 = [
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
        AIMessage(content="Adicionei a pizza margherita ao seu carrinho."),
    ]
    model = ScriptedToolCallingChatModel(responses=responses_turn_1)
    session = Session()
    settings = Settings(_env_file=None)

    chat(model, session, "quero uma pizza margherita", settings)

    assert session.cart.subtotal() > 0
    assert len(session.cart.list_items()) == 1
