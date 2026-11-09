import pytest
from solution import Cart


def test_empty_cart() -> None:
    cart = Cart()
    assert cart.list_items() == []
    assert cart.subtotal() == 0.0


def test_add_new_item() -> None:
    cart = Cart()
    cart.add_item("1", "Produto", 10.0, 2)
    items = cart.list_items()
    assert len(items) == 1
    item = items[0]
    assert item["item_id"] == "1"
    assert item["nome"] == "Produto"
    assert item["preco"] == 10.0
    assert item["quantidade"] == 2
    assert item["subtotal"] == 20.0
    assert cart.subtotal() == 20.0


def test_add_same_item_accumulates_quantity() -> None:
    cart = Cart()
    cart.add_item("1", "Produto", 10.0, 2)
    cart.add_item("1", "OutroNome", 99.0, 3)
    items = cart.list_items()
    assert len(items) == 1
    item = items[0]
    assert item["nome"] == "Produto"
    assert item["preco"] == 10.0
    assert item["quantidade"] == 5
    assert item["subtotal"] == 50.0
    assert cart.subtotal() == 50.0


def test_add_two_different_items() -> None:
    cart = Cart()
    cart.add_item("1", "A", 10.0, 2)
    cart.add_item("2", "B", 5.5, 4)
    items = cart.list_items()
    assert len(items) == 2
    ids = {item["item_id"] for item in items}
    assert ids == {"1", "2"}
    assert cart.subtotal() == pytest.approx(20.0 + 22.0)


def test_remove_existing_item() -> None:
    cart = Cart()
    cart.add_item("1", "A", 10.0, 2)
    assert cart.remove_item("1") is True
    assert cart.list_items() == []
    assert cart.subtotal() == 0.0


def test_remove_nonexistent_item() -> None:
    cart = Cart()
    cart.add_item("1", "A", 10.0, 2)
    before = cart.list_items()
    assert cart.remove_item("999") is False
    assert cart.list_items() == before
    assert cart.subtotal() == 20.0


def test_clear_cart() -> None:
    cart = Cart()
    cart.add_item("1", "A", 10.0, 2)
    cart.add_item("2", "B", 5.0, 1)
    cart.clear()
    assert cart.list_items() == []
    assert cart.subtotal() == 0.0


@pytest.mark.parametrize("quantidade", [0, -1, -10])
def test_invalid_quantity_raises(quantidade: int) -> None:
    cart = Cart()
    with pytest.raises(ValueError):
        cart.add_item("1", "A", 10.0, quantidade)


def test_negative_price_raises() -> None:
    cart = Cart()
    with pytest.raises(ValueError):
        cart.add_item("1", "A", -0.01, 1)


@pytest.mark.parametrize("item_id", ["", "   ", None])
def test_invalid_item_id_raises(item_id) -> None:
    cart = Cart()
    with pytest.raises(ValueError):
        cart.add_item(item_id, "A", 10.0, 1)


@pytest.mark.parametrize("nome", ["", "   ", None])
def test_invalid_nome_raises(nome) -> None:
    cart = Cart()
    with pytest.raises(ValueError):
        cart.add_item("1", nome, 10.0, 1)
