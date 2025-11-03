import pytest
from unittest.mock import MagicMock, patch

from saleor.graphql.product.filters.product_helpers import filter_stocks


@pytest.mark.parametrize(
    "nome_ct, entrada_value, saida_esperada_str",
    [
        # Caso de Teste 1 (CT1):
        ("CT1 - Ambos Falsos", 
         {"warehouse_ids": None, "quantity": None}, 
         "qs"),
        
        # Caso de Teste 2 (CT2):
        ("CT2 - warehouse_ids V, quantity F", 
         {"warehouse_ids": [1], "quantity": None}, 
         "filter_warehouses"),
        
        # Caso de Teste 3 (CT3):
        ("CT3 - warehouse_ids F, quantity V", 
         {"warehouse_ids": None, "quantity": 10}, 
         "filter_quantity"),
        
        # Caso de Teste 4 (CT4):
        ("CT4 - Ambos Verdadeiros", 
         {"warehouse_ids": [1], "quantity": 10}, 
         "filter_quantity"),
    ],
)
def test_filter_stocks_mc_dc(nome_ct, entrada_value, saida_esperada_str, mocker):
    """
    Testa a lógica de decisão do filter_stocks cobrindo todos os 4 
    cenários de combinação de condições (MC/DC)
    """
    
    qs_original = MagicMock(name="queryset_original")
    
    # Patch com caminho correto para as funções
    mocker.patch(
        "saleor.graphql.product.filters.product_helpers.filter_warehouses", 
        return_value="chamou_filter_warehouses"
    )
    mocker.patch(
        "saleor.graphql.product.filters.product_helpers.filter_quantity", 
        return_value="chamou_filter_quantity"
    )

    resultado = filter_stocks(qs_original, None, entrada_value)
    
    if saida_esperada_str == "qs":
        assert resultado is qs_original, f"Falha no {nome_ct}: Esperava 'qs'"
    
    elif saida_esperada_str == "filter_warehouses":
        assert resultado == "chamou_filter_warehouses", f"Falha no {nome_ct}"
    
    elif saida_esperada_str == "filter_quantity":
        assert resultado == "chamou_filter_quantity", f"Falha no {nome_ct}"