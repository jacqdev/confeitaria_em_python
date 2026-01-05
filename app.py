import streamlit as st
import pandas as pd
import io
import os
import matplotlib.pyplot as plt
from fpdf import FPDF

st.title("Confeitaria em Python 🍰")

# ===== 1) Upload ou caminho =====
st.subheader("1) Carregue o arquivo CSV")
arquivo = st.file_uploader("Selecione seu vendas.csv", type=["csv"])
caminho = st.text_input("Ou informe o caminho do arquivo", value="data/vendas.csv")

df = None
if arquivo is not None:
    raw = arquivo.read()
    texto = raw.decode("utf-8", errors="ignore")
    sep = ";" if texto.count(";") > texto.count(",") else ","
    df = pd.read_csv(io.StringIO(texto), sep=sep)
elif caminho:
    try:
        df = pd.read_csv(caminho, encoding="utf-8", sep=",")
    except Exception as e:
        st.error(f"Erro ao carregar CSV: {e}")

if df is None:
    st.stop()

# ===== 2) Mapeamento =====
st.subheader("2) Mapeie as colunas")
opcoes = ["(selecionar)"] + list(df.columns)
col_data = st.selectbox("Coluna de data", opcoes)
col_produto = st.selectbox("Coluna de produto", opcoes)
col_categoria = st.selectbox("Coluna de categoria", opcoes)
col_quantidade = st.selectbox("Coluna de quantidade", opcoes)
col_preco = st.selectbox("Coluna de preço unitário", opcoes)

faltando = [c for c in [col_data, col_produto, col_categoria, col_quantidade, col_preco] if c == "(selecionar)"]
if faltando:
    st.stop()

# ===== 3) Preparar dados =====
df[col_data] = pd.to_datetime(df[col_data], errors="coerce", dayfirst=True)
df[col_quantidade] = pd.to_numeric(df[col_quantidade], errors="coerce")
df[col_preco] = pd.to_numeric(df[col_preco], errors="coerce")
df["faturamento"] = df[col_quantidade].fillna(0) * df[col_preco].fillna(0)

# Filtro de datas
st.subheader("Filtro de período")
data_min, data_max = df[col_data].min(), df[col_data].max()
if pd.isna(data_min) or pd.isna(data_max):
    st.info("Datas inválidas no CSV; exibindo tudo.")
else:
    intervalo = st.date_input("Selecione o intervalo", (data_min, data_max), min_value=data_min, max_value=data_max)
    if isinstance(intervalo, tuple) and len(intervalo) == 2:
        df = df[(df[col_data] >= pd.to_datetime(intervalo[0])) & (df[col_data] <= pd.to_datetime(intervalo[1]))]

# ===== Resumo =====
st.subheader("Resumo")
total_faturamento = float(df["faturamento"].sum())
total_itens = float(df[col_quantidade].sum())
total_registros = int(len(df))
colA, colB, colC = st.columns(3)
colA.metric("💰 Faturamento total", f"R$ {total_faturamento:,.2f}")
colB.metric("📦 Unidades vendidas", f"{int(total_itens)}")
colC.metric("📝 Registros", f"{total_registros}")

# ===== Rankings =====
st.subheader("🏆 Top 5 Produtos Mais Vendidos")
st.table(df.groupby(col_produto)[col_quantidade].sum().sort_values(ascending=False).head(5))

st.subheader("🏆 Top 5 Categorias Mais Vendidas")
st.table(df.groupby(col_categoria)[col_quantidade].sum().sort_values(ascending=False).head(5))

# ===== Gráficos =====
st.subheader("🍩 Faturamento por produto")
st.bar_chart(df.groupby(col_produto)["faturamento"].sum().sort_values(ascending=False))

st.subheader("📂 Faturamento por categoria")
st.bar_chart(df.groupby(col_categoria)["faturamento"].sum().sort_values(ascending=False))

st.subheader("📅 Faturamento por data")
st.line_chart(df.groupby(col_data)["faturamento"].sum().sort_index())

# Gráfico de pizza robusto
st.subheader("🥧 Participação das Categorias no Faturamento")
graf_pizza = df.groupby(col_categoria)["faturamento"].sum()
graf_pizza = graf_pizza.replace([float("inf"), -float("inf")], pd.NA).dropna()
graf_pizza = graf_pizza[graf_pizza > 0]
if graf_pizza.empty:
    st.info("Não há faturamento válido para mostrar no gráfico de pizza.")
else:
    fig, ax = plt.subplots(figsize=(6, 6))
    graf_pizza.plot.pie(autopct="%1.1f%%", ylabel="", ax=ax)
    st.pyplot(fig)

# ===== Exportar Excel =====
buffer = io.BytesIO()
try:
    df.to_excel(buffer, index=False, engine="openpyxl")
    st.download_button(
        "📤 Baixar Excel",
        buffer.getvalue(),
        "relatorio_vendas.xlsx",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
except Exception as e:
    st.error(f"Falha ao gerar Excel: {e}")
    alt_csv = io.StringIO()
    df.to_csv(alt_csv, index=False)
    st.download_button("📤 Baixar CSV (alternativo)", alt_csv.getvalue(), "relatorio_vendas.csv", "text/csv")

# ===== Exportar PDF (com fallback de fonte) =====
def sanitize_text(s: str) -> str:
    # Remove caracteres que podem quebrar a fonte básica
    try:
        return s
    except Exception:
        return str(s)

def gerar_pdf(df_local):
    pdf = FPDF()
    pdf.add_page()

    # Tenta usar fonte Unicode (DejaVu); se não existir, usa Arial (Latin-1)
    font_path = "DejaVuSans.ttf"
    has_unicode = os.path.exists(font_path)
    if has_unicode:
        pdf.add_font("DejaVu", "", font_path, uni=True)
        pdf.set_font("DejaVu", size=12)
    else:
        pdf.set_font("Arial", size=12)

    # Título
    titulo = "Relatório de Vendas - Confeitaria 🍰" if has_unicode else "Relatorio de Vendas - Confeitaria"
    pdf.cell(0, 10, titulo, ln=True, align="C")
    pdf.ln(8)

    # Resumo
    lin1 = f"💰 Faturamento total: R$ {total_faturamento:,.2f}" if has_unicode else f"Faturamento total: R$ {total_faturamento:,.2f}"
    lin2 = f"📦 Unidades vendidas: {int(total_itens)}" if has_unicode else f"Unidades vendidas: {int(total_itens)}"
    lin3 = f"📝 Registros: {total_registros}" if has_unicode else f"Registros: {total_registros}"
    pdf.cell(0, 8, sanitize_text(lin1), ln=True)
    pdf.cell(0, 8, sanitize_text(lin2), ln=True)
    pdf.cell(0, 8, sanitize_text(lin3), ln=True)
    pdf.ln(6)

    # Top 5 Produtos
    pdf.cell(0, 8, "🏆 Top 5 Produtos:" if has_unicode else "Top 5 Produtos:", ln=True)
    top_prod = df_local.groupby(col_produto)[col_quantidade].sum().sort_values(ascending=False).head(5)
    for p, q in top_prod.items():
        pdf.cell(0, 8, sanitize_text(f"- {p}: {int(q)}"), ln=True)

    pdf.ln(4)
    # Top 5 Categorias
    pdf.cell(0, 8, "🏆 Top 5 Categorias:" if has_unicode else "Top 5 Categorias:", ln=True)
    top_cat = df_local.groupby(col_categoria)[col_quantidade].sum().sort_values(ascending=False).head(5)
    for c, q in top_cat.items():
        pdf.cell(0, 8, sanitize_text(f"- {c}: {int(q)}"), ln=True)

    # Saída: codificação conforme fonte utilizada
    if has_unicode:
        return pdf.output(dest="S").encode("utf-8")
    else:
        return pdf.output(dest="S").encode("latin-1", errors="ignore")

try:
    pdf_bytes = gerar_pdf(df)
    st.download_button("📄 Baixar PDF", pdf_bytes, "relatorio_vendas.pdf", "application/pdf")
except Exception as e:
    st.error(f"Falha ao gerar PDF: {e}")
    st.info("Se quiser emojis/acentos no PDF, coloque o arquivo DejaVuSans.ttf na mesma pasta do app.")
