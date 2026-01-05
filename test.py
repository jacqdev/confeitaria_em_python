import streamlit as st
import pandas as pd

st.title("Confeitaria em Python 🍰")

# ----- Carregamento -----
def carregar_csv(caminho: str) -> pd.DataFrame | None:
    try:
        return pd.read_csv(caminho, encoding="utf-8", sep=",")
    except UnicodeDecodeError:
        try:
            return pd.read_csv(caminho, encoding="latin-1", sep=",")
        except Exception as e2:
            st.error(f"Erro de encoding ao abrir {caminho}: {e2}")
            return None
    except FileNotFoundError:
        st.error(f"Arquivo não encontrado: {caminho}")
        return None
    except Exception as e:
        st.error(f"Falha ao ler {caminho}: {e}")
        return None

# Entrada do caminho (já apontando para a pasta data)
caminho = st.text_input("Caminho do CSV de vendas", value="data/vendas.csv")

vendas = carregar_csv(caminho)

if vendas is None:
    st.stop()

st.success(f"CSV carregado! Linhas: {len(vendas)} | Colunas: {list(vendas.columns)}")

# ----- Normalização de colunas -----
def encontrar_coluna(opcoes):
    cols_lower = {c.lower(): c for c in vendas.columns}
    for nome in opcoes:
        if nome.lower()