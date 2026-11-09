from foodagent.catalog import buscar_item_por_id, buscar_no_catalogo, catalogo_padrao

CATALOGO = [
    {
        "item_id": "a",
        "nome": "Pizza Margherita",
        "categoria": "pizza",
        "preco": 40.0,
        "vegetariano": True,
    },
    {
        "item_id": "b",
        "nome": "Pizza Pepperoni",
        "categoria": "pizza",
        "preco": 50.0,
        "vegetariano": False,
    },
    {
        "item_id": "c",
        "nome": "Burger Veggie",
        "categoria": "hamburguer",
        "preco": 30.0,
        "vegetariano": True,
    },
]


def test_busca_por_texto_case_insensitive():
    resultado = buscar_no_catalogo(CATALOGO, query="pizza")
    assert {item["item_id"] for item in resultado} == {"a", "b"}


def test_busca_sem_filtro_retorna_tudo():
    assert len(buscar_no_catalogo(CATALOGO)) == 3


def test_filtro_categoria():
    resultado = buscar_no_catalogo(CATALOGO, categoria="hamburguer")
    assert [item["item_id"] for item in resultado] == ["c"]


def test_filtro_vegetariano():
    resultado = buscar_no_catalogo(CATALOGO, vegetariano=True)
    assert {item["item_id"] for item in resultado} == {"a", "c"}


def test_filtro_preco_maximo():
    resultado = buscar_no_catalogo(CATALOGO, preco_max=35.0)
    assert [item["item_id"] for item in resultado] == ["c"]


def test_filtros_combinados():
    resultado = buscar_no_catalogo(CATALOGO, categoria="pizza", vegetariano=True)
    assert [item["item_id"] for item in resultado] == ["a"]


def test_busca_sem_correspondencia_retorna_vazio():
    assert buscar_no_catalogo(CATALOGO, query="sushi") == []


def test_busca_nao_modifica_catalogo_original():
    original = [dict(item) for item in CATALOGO]
    buscar_no_catalogo(CATALOGO, categoria="pizza")
    assert CATALOGO == original


def test_buscar_item_por_id_encontrado():
    item = buscar_item_por_id(CATALOGO, "b")
    assert item is not None
    assert item["nome"] == "Pizza Pepperoni"


def test_buscar_item_por_id_nao_encontrado():
    assert buscar_item_por_id(CATALOGO, "inexistente") is None


def test_catalogo_padrao_carrega_do_json():
    catalogo = catalogo_padrao()
    assert len(catalogo) > 0
    assert all("item_id" in item for item in catalogo)
