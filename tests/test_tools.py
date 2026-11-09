from foodagent.cart import Cart
from foodagent.config import Settings
from foodagent.tools import make_tools

CATALOGO = [
    {
        "item_id": "pizza-1",
        "nome": "Pizza Margherita",
        "categoria": "pizza",
        "preco": 40.0,
        "vegetariano": True,
    },
    {
        "item_id": "burger-1",
        "nome": "Burger Clássico",
        "categoria": "hamburguer",
        "preco": 30.0,
        "vegetariano": False,
    },
]


def _tools() -> dict:
    cart = Cart()
    settings = Settings(_env_file=None)
    tools = make_tools(cart, CATALOGO, settings)
    return {t.name: t for t in tools}, cart


def test_buscar_cardapio_filtra_por_texto():
    tools, _ = _tools()
    resultado = tools["buscar_cardapio"].invoke({"query": "pizza"})
    assert [item["item_id"] for item in resultado] == ["pizza-1"]


def test_adicionar_ao_carrinho_item_existente():
    tools, cart = _tools()
    resultado = tools["adicionar_ao_carrinho"].invoke({"item_id": "pizza-1", "quantidade": 2})
    assert resultado["ok"] is True
    assert cart.subtotal() == 80.0


def test_adicionar_ao_carrinho_item_inexistente():
    tools, cart = _tools()
    resultado = tools["adicionar_ao_carrinho"].invoke({"item_id": "inexistente"})
    assert "erro" in resultado
    assert cart.list_items() == []


def test_remover_do_carrinho():
    tools, cart = _tools()
    tools["adicionar_ao_carrinho"].invoke({"item_id": "burger-1"})
    resultado = tools["remover_do_carrinho"].invoke({"item_id": "burger-1"})
    assert resultado["removido"] is True
    assert cart.list_items() == []


def test_ver_carrinho():
    tools, _ = _tools()
    tools["adicionar_ao_carrinho"].invoke({"item_id": "pizza-1", "quantidade": 1})
    resultado = tools["ver_carrinho"].invoke({})
    assert resultado["subtotal"] == 40.0
    assert len(resultado["itens"]) == 1


def test_calcular_total_inclui_taxa_de_entrega():
    tools, _ = _tools()
    tools["adicionar_ao_carrinho"].invoke({"item_id": "pizza-1", "quantidade": 1})
    resultado = tools["calcular_total"].invoke({"distancia_km": 5})
    assert resultado["subtotal"] == 40.0
    assert resultado["taxa_entrega"] == 11.0
    assert resultado["total"] == 51.0
