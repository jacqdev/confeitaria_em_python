import pandas as pd
from src.visualizacao import grafico_faturamento

def test_grafico_faturamento():
    df = pd.DataFrame({"Mes": ["Jan", "Fev"], "Faturamento": [100, 200]})
    fig = grafico_faturamento(df)
    assert fig is not None
    assert fig.axes[0].get_title() == "Faturamento Mensal"
