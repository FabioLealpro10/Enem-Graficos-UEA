import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def dashboard_climatico():

    st.set_page_config(page_title="Dashboard Climático", layout="wide")
    st.title("🌦 Dashboard Climático com Análise Diária")

    caminho_csv = "Geina.csv"  # 🔥 ALTERE AQUI

    try:
        df = pd.read_csv(caminho_csv, sep=";", decimal=",")
    except Exception as e:
        st.error(f"Erro ao carregar o arquivo: {e}")
        return

    # =========================
    # LIMPEZA
    # =========================
    df.columns = df.columns.str.strip().str.lower()

    if "data" not in df.columns or "hora (utc)" not in df.columns:
        st.error("Colunas 'data' ou 'hora (utc)' não encontradas.")
        return

    df["data"] = df["data"].astype(str)
    df["hora (utc)"] = df["hora (utc)"].astype(str)

    df["datetime"] = pd.to_datetime(
        df["data"] + " " + df["hora (utc)"],
        dayfirst=True,
        errors="coerce"
    )

    df = df.dropna(subset=["datetime"])
    df = df.sort_values("datetime")
    df = df.set_index("datetime")

    # Converter colunas numéricas
    for col in df.columns:
        if col not in ["data", "hora (utc)"]:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # =========================
    # FILTRO POR PERÍODO
    # =========================
    st.sidebar.header("📅 Filtro por Período")

    data_inicio = st.sidebar.date_input("Data Inicial", df.index.min().date())
    data_fim = st.sidebar.date_input("Data Final", df.index.max().date())

    df_filtrado = df.loc[str(data_inicio):str(data_fim)]

    if df_filtrado.empty:
        st.warning("Sem dados no período selecionado.")
        return

    # =========================
    # AGREGAÇÃO DIÁRIA
    # =========================
    df_filtrado["data_dia"] = df_filtrado.index.date

    df_diario = df_filtrado.groupby("data_dia").agg({
        "temp. max. (c)": "mean",
        "temp. min. (c)": "mean",
        "temp. ins. (c)": "mean",
        "chuva (mm)": "sum",
        "umi. ins. (%)": "mean",
        "pressao ins. (hpa)": "mean"
    })

    df_diario = df_diario.dropna(how="all")

    st.subheader("📋 Dados Diários")
    st.dataframe(df_diario.head())

    quantidade_dias = len(df_diario)

    # =========================
    # 🌡 TEMPERATURA MÁX E MÍN
    # =========================
    st.subheader("🌡 Média Diária de Temperatura Máxima e Mínima")

    fig1, ax1 = plt.subplots(figsize=(12,5))

    df_diario[["temp. max. (c)", "temp. min. (c)"]].plot(ax=ax1)

    ax1.set_ylabel("Temperatura (°C)")
    ax1.set_title("Temperatura Máxima e Mínima Diária")

    plt.xticks(rotation=45)

    st.pyplot(fig1)

    # =========================
    # 🌧 CHUVA POR DIA (INTELIGENTE)
    # =========================
    st.subheader("🌧 Quantidade de Chuva por Dia")

    fig2, ax2 = plt.subplots(figsize=(12,5))

    if quantidade_dias <= 15:
        # Barras se poucos dias
        df_diario["chuva (mm)"].plot(kind="bar", ax=ax2)
    else:
        # Linha se muitos dias
        df_diario["chuva (mm)"].plot(ax=ax2)

    ax2.set_ylabel("Chuva (mm)")
    ax2.set_title("Chuva Diária")

    # Ajuste inteligente de datas
    passo = max(1, quantidade_dias // 10)
    ax2.set_xticks(range(0, quantidade_dias, passo))
    ax2.set_xticklabels(
        df_diario.index[::passo],
        rotation=45,
        ha="right"
    )

    st.pyplot(fig2)

    # =========================
    # 🌡 TEMPERATURA MÉDIA DIÁRIA
    # =========================
    st.subheader("🌡 Temperatura Média Diária")

    fig3, ax3 = plt.subplots(figsize=(12,5))

    df_diario["temp. ins. (c)"].plot(ax=ax3)

    ax3.set_ylabel("Temperatura (°C)")
    ax3.set_title("Temperatura Média Diária")

    plt.xticks(rotation=45)

    st.pyplot(fig3)

    # =========================
    # 💧 UMIDADE E PRESSÃO
    # =========================
    st.subheader("💧 Umidade e Pressão Média Diária")

    fig4, ax4 = plt.subplots(figsize=(12,5))

    df_diario[["umi. ins. (%)", "pressao ins. (hpa)"]].plot(ax=ax4)

    ax4.set_title("Umidade e Pressão Diária")

    plt.xticks(rotation=45)

    st.pyplot(fig4)


if __name__ == "__main__":
    dashboard_climatico()