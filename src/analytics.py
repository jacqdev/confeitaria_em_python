import pandas as pd

def calcular_media(valores):
    if valores is None or len(valores) == 0:
        return 0
    return sum(valores) / len(valores)

def kpis(df: pd.DataFrame) -> dict:
    faturamento_total = df["faturamento"].sum()
    itens_vendidos = df["quantidade"].sum()
    ticket_medio = faturamento_total / itens_vendidos if itens_vendidos > 0 else 0

    mensal = df.groupby(["ano","mes"], as_index=False)["faturamento"].sum().sort_values(["ano","mes"])
    if len(mensal) >= 2 and mensal.iloc[-2]["faturamento"] > 0:
        crescimento = (mensal.iloc[-1]["faturamento"] - mensal.iloc[-2]["faturamento"]) / mensal.iloc[-2]["faturamento"] * 100
    else:
        crescimento = 0

    return {
        "faturamento_total": faturamento_total,
        "itens_vendidos": itens_vendidos,
        "ticket_medio": ticket_medio,
        "crescimento_mensal_pct": crescimento
    }

def top_produtos(df: pd.DataFrame, n=5) -> pd.DataFrame:
    return df.groupby("produto", as_index=False)["faturamento"].sum().sort_values("faturamento", ascending=False).head(n)

def mensal_por_ano(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby(["ano","mes_nome"], as_index=False)["faturamento"].sum()
