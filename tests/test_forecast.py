import pandas as pd
from src.forecast import preparar_mensal, prever_linear, combinar_hist_prev

def test_preparar_mensal():
    df = pd.DataFrame({
        "ano": [2025, 2025],
        "mes": [1, 2],
        "faturamento": [100, 200]
    })
    mensal = preparar_mensal(df)
    assert "valor" in mensal.columns
    assert "tipo" in mensal.columns
    assert mensal["tipo"].iloc[0] == "Histórico"

def test_prever_linear_mes_normal():
    # último mês não é dezembro → caminho normal
    df = pd.DataFrame({
        "ano": [2025],
        "mes": [5],
        "faturamento": [100]
    })
    mensal = preparar_mensal(df)
    futuro, modelo = prever_linear(mensal, passos=2)
    assert len(futuro) == 2
    assert all(futuro["tipo"] == "Previsão")

def test_prever_linear_ano_novo():
    # último mês é dezembro → força o caminho do if mes > 12
    df = pd.DataFrame({
        "ano": [2025],
        "mes": [12],
        "faturamento": [100]
    })
    mensal = preparar_mensal(df)
    futuro, modelo = prever_linear(mensal, passos=2)

    # primeira previsão deve ser janeiro de 2026
    assert futuro.iloc[0]["ano"] == 2026
    assert futuro.iloc[0]["mes"] == 1
    assert all(futuro["tipo"] == "Previsão")

def test_combinar_hist_prev():
    hist = pd.DataFrame({
        "ano": [2025],
        "mes": [1],
        "faturamento": [100],
        "valor": [100],
        "tipo": ["Histórico"]
    })
    futuro = pd.DataFrame({
        "ano": [2025],
        "mes": [2],
        "valor": [120],
        "tipo": ["Previsão"]
    })
    combinado = combinar_hist_prev(hist, futuro)
    assert len(combinado) == 2
    assert "tipo" in combinado.columns
