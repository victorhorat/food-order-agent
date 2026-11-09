import pytest

from foodagent.delivery import calcular_taxa_entrega


def test_taxa_entrega_distancia_zero():
    assert calcular_taxa_entrega(0) == 5.00


def test_taxa_entrega_com_distancia():
    assert calcular_taxa_entrega(10) == 17.00


def test_taxa_entrega_com_taxas_customizadas():
    assert calcular_taxa_entrega(5, taxa_fixa=3.0, taxa_por_km=2.0) == 13.00


def test_taxa_entrega_arredonda_duas_casas():
    assert calcular_taxa_entrega(1.333, taxa_fixa=5.0, taxa_por_km=1.0) == 6.33


def test_taxa_entrega_distancia_negativa_levanta_erro():
    with pytest.raises(ValueError):
        calcular_taxa_entrega(-1)


@pytest.mark.parametrize("distancia", [None, "10", True])
def test_taxa_entrega_tipo_invalido_levanta_erro(distancia):
    with pytest.raises(ValueError):
        calcular_taxa_entrega(distancia)
