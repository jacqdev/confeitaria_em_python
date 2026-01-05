import pandas as pd
from sklearn.linear_model import LinearRegression

def preparar_mensal(df: pd.DataFrame) -> pd.DataFrame:
    mensal = df.groupby(["ano", "mes"])["faturamento"].sum().reset_index()
    mensal["valor"] = mensal["faturamento"]
    mensal["tipo"] = "Histórico"
    return mensal

def prever_linear(mensal: pd.DataFrame, passos: int = 3):
    X = mensal[["ano", "mes"]]
    y = mensal["valor"]

    modelo = LinearRegression()
    modelo.fit(X, y)

    ultimo_ano, ultimo_mes = X.iloc[-1]
    futuros = []
    for i in range(1, passos + 1):
        mes = ultimo_mes + i
        ano = ultimo_ano
        if mes > 12:
            mes -= 12
            ano += 1
        futuros.append([ano, mes])

    futuro_df = pd.DataFrame(futuros, columns=["ano", "mes"])
    futuro_df["valor"] = modelo.predict(futuro_df)
    futuro_df["tipo"] = "Previsão"

    return futuro_df, modelo

def combinar_hist_prev(mensal: pd.DataFrame, futuro: pd.DataFrame) -> pd.DataFrame:
    combinado = pd.concat([mensal, futuro], ignore_index=True)
    return combinado
