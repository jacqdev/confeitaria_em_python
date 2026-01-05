import pandas as pd

def limpar_nulos(df: pd.DataFrame) -> pd.DataFrame:
    return df.dropna()

def normalizar_colunas(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = [c.strip().lower() for c in df.columns]
    return df
