 # confeitaria_em_python 🍰

Projeto em Python para simular e analisar dados de faturamento de uma confeitaria.  
Inclui coleta de dados, tratamento, testes automatizados e visualizações gráficas.

## Como rodar
```bash
pip install -r requirements.txt
python main.py
pytest


---

### `main.py`
```python
import pandas as pd
from src import coleta, tratamento, visualizacao

# 1. Coleta de dados (simulação de faturamento mensal)
df = coleta.simular_faturamento()

# 2. Tratamento dos dados
df_limpo = tratamento.limpar_dados(df)

# 3. Estatísticas básicas
print("Média:", df_limpo["Faturamento"].mean())
print("Máximo:", df_limpo["Faturamento"].max())
print("Mínimo:", df_limpo["Faturamento"].min())

# 4. Visualizações
visualizacao.grafico_linha(df_limpo, "Mes", "Faturamento", "Faturamento Mensal")
visualizacao.grafico_barras(df_limpo, "Mes", "Faturamento", "Comparativo Mensal")
