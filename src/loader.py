import pandas as pd

def carregar_dados_csv(path: str) -> pd.DataFrame:
    """
    Carrega o CSV de vendas e adiciona colunas derivadas.
    Espera colunas: data, produto, categoria, quantidade, preco
    """
    try:
        df = pd.read_csv(path, parse_dates=["data"], encoding="utf-8")
    except UnicodeDecodeError:
        df = pd.read_csv(path, parse_dates=["data"], encoding="latin1")

    colunas_necessarias = {"data", "produto", "categoria", "quantidade", "preco"}
    if not colunas_necessarias.issubset(df.columns):
        raise ValueError(f"CSV deve conter as colunas obrigatórias: {colunas_necessarias}")

    df["faturamento"] = df["quantidade"] * df["preco"]
    df["ano"] = df["data"].dt.year
    df["mes"] = df["data"].dt.month
    df["mes_nome"] = df["data"].dt.strftime("%b")

    return df
