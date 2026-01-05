import pandas as pd
from src.analytics import calcular_media, kpis, top_produtos, mensal_por_ano

def test_calcular_media():
    assert calcular_media([10, 20, 30]) == 20
    assert calcular_media([]) == 0
    assert calcular_media(None) == 0

def test_kpis_crescimento_normal():
    df = pd.DataFrame({
        "ano": [2025, 2025],
        "mes": [1, 2],
        "mes_nome": ["Jan", "Fev"],
        "quantidade": [10, 20],
        "faturamento": [100.0, 400.0],
        "produto": ["bolo", "torta"]
    })
    resultado = kpis(df)
    assert resultado["faturamento_total"] == 500.0
    assert resultado["itens_vendidos"] == 30
    assert resultado["ticket_medio"] == 500.0 / 30
    assert resultado["crescimento_mensal_pct"] == 300.0

def test_kpis_crescimento_zero():
    # força o caminho do else (linha 17)
    df = pd.DataFrame({
        "ano": [2025],
        "mes": [1],
        "mes_nome": ["Jan"],
        "quantidade": [10],
        "faturamento": [0.0],
        "produto": ["bolo"]
    })
    resultado = kpis(df)
    assert resultado["crescimento_mensal_pct"] == 0

def test_top_produtos():
    df = pd.DataFrame({"produto": ["bolo", "torta"], "faturamento": [200.0, 500.0]})
    top = top_produtos(df, n=1)
    assert top.iloc[0]["produto"] == "torta"

def test_mensal_por_ano():
    df = pd.DataFrame({"ano": [2025, 2025], "mes_nome": ["Jan", "Jan"], "faturamento": [100.0, 200.0]})
    mensal = mensal_por_ano(df)
    assert mensal.iloc[0]["faturamento"] == 300.0
