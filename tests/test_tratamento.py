import pandas as pd
from src.tratamento import limpar_nulos, normalizar_colunas

def test_limpar_nulos():
    df = pd.DataFrame({"produto": ["bolo", None], "quantidade": [10, None]})
    df_limpo = limpar_nulos(df)
    assert df_limpo.isnull().sum().sum() == 0

def test_normalizar_colunas():
    df = pd.DataFrame({" Produto ": [1]})
    df_norm = normalizar_colunas(df)
    assert "produto" in df_norm.columns
