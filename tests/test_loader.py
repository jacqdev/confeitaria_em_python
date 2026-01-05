import pandas as pd
import pytest
from src.loader import carregar_dados_csv   # IMPORT ESSENCIAL

def test_carregar_dados_csv_valido(tmp_path):
    file = tmp_path / "dados.csv"
    df = pd.DataFrame({
        "data": pd.to_datetime(["2025-01-01", "2025-02-01"]),
        "produto": ["bolo", "torta"],
        "categoria": ["doce", "doce"],
        "quantidade": [10, 20],
        "preco": [5.0, 7.5]
    })
    df.to_csv(file, index=False)
    dados = carregar_dados_csv(file)
    assert "faturamento" in dados.columns
    assert dados["faturamento"].iloc[0] == 50.0

def test_carregar_dados_csv_invalido(tmp_path):
    file = tmp_path / "dados_invalidos.csv"
    df = pd.DataFrame({"data": pd.to_datetime(["2025-01-01"]), "produto": ["bolo"]})
    df.to_csv(file, index=False)
    with pytest.raises(ValueError):
        carregar_dados_csv(file)

def test_carregar_dados_csv_encoding_fallback(monkeypatch, tmp_path):
    file = tmp_path / "dados_dummy.csv"

    def fake_read_csv(path, parse_dates=None, encoding=None):
        if encoding == "utf-8":
            raise UnicodeDecodeError("utf-8", b"", 0, 1, "invalid start byte")
        return pd.DataFrame({
            "data": pd.to_datetime(["2025-01-01"]),
            "produto": ["bolo especial"],
            "categoria": ["doce"],
            "quantidade": [10],
            "preco": [5.0]
        })

    monkeypatch.setattr(pd, "read_csv", fake_read_csv)
    dados = carregar_dados_csv(file)
    assert "faturamento" in dados.columns
    assert dados["faturamento"].iloc[0] == 50.0
