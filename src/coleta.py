import pandas as pd

def simular_faturamento():
    meses = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun",
             "Jul", "Ago", "Set", "Out", "Nov", "Dez"]
    valores = [10200, 15000, 17800, 22000, 19500, 25000,
               24000, 21000, 18500, 20000, 23000, 24800]

    df = pd.DataFrame({"Mes": meses, "Faturamento": valores})
    return df
