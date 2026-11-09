from __future__ import annotations

import json
from functools import lru_cache
from importlib import resources


def carregar_catalogo() -> list[dict]:
    return json.loads(resources.files("foodagent.data").joinpath("menu.json").read_text("utf-8"))


@lru_cache(maxsize=1)
def catalogo_padrao() -> list[dict]:
    return carregar_catalogo()


def buscar_no_catalogo(
    catalogo: list[dict],
    query: str = "",
    categoria: str | None = None,
    vegetariano: bool | None = None,
    preco_max: float | None = None,
) -> list[dict]:
    query_normalizada = query.strip().lower()
    resultado = []
    for item in catalogo:
        if query_normalizada and query_normalizada not in item["nome"].lower():
            continue
        if categoria is not None and item["categoria"].lower() != categoria.lower():
            continue
        if vegetariano is not None and item["vegetariano"] != vegetariano:
            continue
        if preco_max is not None and item["preco"] > preco_max:
            continue
        resultado.append(dict(item))
    return resultado


def buscar_item_por_id(catalogo: list[dict], item_id: str) -> dict | None:
    for item in catalogo:
        if item["item_id"] == item_id:
            return dict(item)
    return None
