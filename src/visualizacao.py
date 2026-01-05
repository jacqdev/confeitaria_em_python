import matplotlib.pyplot as plt
import pandas as pd

def grafico_faturamento(df: pd.DataFrame, coluna_mes="Mes", coluna_valor="Faturamento"):
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(df[coluna_mes], df[coluna_valor], marker="o", color="blue", linestyle="-")
    ax.set_title("Faturamento Mensal", fontsize=14, fontweight="bold")
    ax.set_xlabel("Mês", fontsize=12)
    ax.set_ylabel("Faturamento", fontsize=12)
    ax.grid(True, linestyle="--", alpha=0.7)
    plt.xticks(rotation=45)
    return fig
