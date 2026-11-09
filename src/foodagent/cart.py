from __future__ import annotations


class Cart:
    def __init__(self) -> None:
        self._items: dict[str, dict] = {}

    def add_item(self, item_id: str, nome: str, preco: float, quantidade: int) -> None:
        if not isinstance(item_id, str) or not item_id.strip():
            raise ValueError("item_id must be a non-empty string")
        if not isinstance(nome, str) or not nome.strip():
            raise ValueError("nome must be a non-empty string")
        if isinstance(preco, bool) or not isinstance(preco, (int, float)) or preco < 0:
            raise ValueError("preco must be a non-negative number")
        if isinstance(quantidade, bool) or not isinstance(quantidade, int) or quantidade <= 0:
            raise ValueError("quantidade must be a positive integer")

        if item_id in self._items:
            self._items[item_id]["quantidade"] += quantidade
        else:
            self._items[item_id] = {
                "item_id": item_id,
                "nome": nome,
                "preco": float(preco),
                "quantidade": quantidade,
            }

    def remove_item(self, item_id: str) -> bool:
        if item_id in self._items:
            del self._items[item_id]
            return True
        return False

    def list_items(self) -> list[dict]:
        return [
            {
                "item_id": item["item_id"],
                "nome": item["nome"],
                "preco": item["preco"],
                "quantidade": item["quantidade"],
                "subtotal": item["preco"] * item["quantidade"],
            }
            for item in self._items.values()
        ]

    def subtotal(self) -> float:
        return sum(item["preco"] * item["quantidade"] for item in self._items.values())

    def clear(self) -> None:
        self._items.clear()
