from langchain_core.tools import tool

from foodagent.cart import Cart
from foodagent.catalog import buscar_item_por_id, buscar_no_catalogo
from foodagent.config import Settings
from foodagent.delivery import calcular_taxa_entrega


def make_tools(cart: Cart, catalogo: list[dict], settings: Settings) -> list:
    @tool
    def buscar_cardapio(
        query: str = "",
        categoria: str | None = None,
        vegetariano: bool | None = None,
        preco_max: float | None = None,
    ) -> list[dict]:
        """Busca itens no cardapio por texto no nome, categoria, se e vegetariano
        e preco maximo. Todos os filtros sao opcionais. Use antes de adicionar
        qualquer item ao carrinho, para confirmar que ele existe e saber o preco."""
        return buscar_no_catalogo(
            catalogo, query=query, categoria=categoria, vegetariano=vegetariano, preco_max=preco_max
        )

    @tool
    def adicionar_ao_carrinho(item_id: str, quantidade: int = 1) -> dict:
        """Adiciona um item do cardapio ao carrinho pelo item_id (obtido via
        buscar_cardapio). Nunca invente um item_id."""
        item = buscar_item_por_id(catalogo, item_id)
        if item is None:
            return {"erro": f"item_id '{item_id}' nao encontrado no cardapio"}
        cart.add_item(
            item_id=item["item_id"], nome=item["nome"], preco=item["preco"], quantidade=quantidade
        )
        return {"ok": True, "item": item["nome"], "quantidade": quantidade}

    @tool
    def remover_do_carrinho(item_id: str) -> dict:
        """Remove um item do carrinho pelo item_id."""
        return {"removido": cart.remove_item(item_id)}

    @tool
    def ver_carrinho() -> dict:
        """Retorna os itens atuais do carrinho e o subtotal."""
        return {"itens": cart.list_items(), "subtotal": cart.subtotal()}

    @tool
    def calcular_total(distancia_km: float) -> dict:
        """Calcula o total do pedido (subtotal do carrinho + taxa de entrega)
        dada a distancia em km até o endereço de entrega."""
        taxa = calcular_taxa_entrega(
            distancia_km, settings.taxa_entrega_fixa, settings.taxa_entrega_por_km
        )
        subtotal = cart.subtotal()
        return {"subtotal": subtotal, "taxa_entrega": taxa, "total": round(subtotal + taxa, 2)}

    return [
        buscar_cardapio,
        adicionar_ao_carrinho,
        remover_do_carrinho,
        ver_carrinho,
        calcular_total,
    ]
