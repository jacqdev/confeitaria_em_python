import pandas as pd

def calcular_resumo(df, col_quantidade, col_preco):
    df["faturamento"] = df[col_quantidade].fillna(0) * df[col_preco].fillna(0)
    total_faturamento = df["faturamento"].sum()
    total_itens = df[col_quantidade].sum()
    total_registros = len(df)
    return total_faturamento, total_itens, total_registros

def top_n(df, coluna, col_quantidade, n=5):
    return df.groupby(coluna)[col_quantidade].sum().sort_values(ascending=False).head(n)
