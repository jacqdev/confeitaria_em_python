import pandas as pd
from utils import calcular_resumo, top_n

def test_calcular_resumo():
    df = pd.DataFrame({"produto": ["bolo"], "quantidade": [10], "preco": [20.0]})
    total_faturamento, total_itens, total_registros = calcular_resumo(df, "quantidade", "preco")
    assert total_faturamento == 200
    assert total_itens == 10
    assert total_registros == 1

def test_top_n():
    df = pd.DataFrame({"produto": ["bolo", "torta"], "quantidade": [10, 20]})
    top = top_n(df, "produto", "quantidade", n=1)
    assert top.index[0] == "torta"
