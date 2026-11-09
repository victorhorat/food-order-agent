from __future__ import annotations


def calcular_taxa_entrega(
    distancia_km: float,
    taxa_fixa: float = 5.00,
    taxa_por_km: float = 1.20,
) -> float:
    if isinstance(distancia_km, bool) or not isinstance(distancia_km, (int, float)):
        raise ValueError("distancia_km deve ser um número")
    if distancia_km < 0:
        raise ValueError("distancia_km não pode ser negativa")
    if isinstance(taxa_fixa, bool) or not isinstance(taxa_fixa, (int, float)) or taxa_fixa < 0:
        raise ValueError("taxa_fixa deve ser um número não-negativo")
    if (
        isinstance(taxa_por_km, bool)
        or not isinstance(taxa_por_km, (int, float))
        or taxa_por_km < 0
    ):
        raise ValueError("taxa_por_km deve ser um número não-negativo")

    return round(taxa_fixa + taxa_por_km * distancia_km, 2)
