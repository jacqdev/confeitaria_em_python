from src import coleta

def test_faturamento_positivo():
    df = coleta.simular_faturamento()
    assert (df["Faturamento"] >= 0).all()
    assert len(df) == 12
