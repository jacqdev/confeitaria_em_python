import pandas as pd
from src import coleta, tratamento, visualizacao

def main():
    df = coleta.simular_faturamento()
    df_limpo = tratamento.limpar_dados(df)

    print("📊 Estatísticas do Faturamento")
    print("- Média:", df_limpo["Faturamento"].mean())
    print("- Máximo:", df_limpo["Faturamento"].max())
    print("- Mínimo:", df_limpo["Faturamento"].min())

    visualizacao.grafico_linha(df_limpo, "Mes", "Faturamento", "Faturamento Mensal")
    visualizacao.grafico_barras(df_limpo, "Mes", "Faturamento", "Comparativo Mensal")

if __name__ == "__main__":
    main()
