import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def dashboard_climatico():

    st.set_page_config(page_title="Análise Climática", layout="wide")
    st.title("🌦 Análise Climática")

    caminho_csv = "/home/fabio-leal/Python/Enem-Graficos-UEA-main/app/zInutes/planilhaMatheus.csv"  # 🔥 ALTERE AQUI

    try:
        df = pd.read_csv(caminho_csv, sep=",", decimal=".")
    except Exception as e:
        st.error(f"Erro ao carregar o arquivo: {e}")
        return

    # Mostrar colunas para debug
    st.write("Colunas encontradas:", df.columns)

    # Limpeza
    df.columns = df.columns.str.strip()

    if "Data" not in df.columns:
        st.error("Coluna 'Data' não encontrada.")
        return

    # Converter data
    df["Data"] = pd.to_datetime(df["Data"], dayfirst=True, errors="coerce")

    # Converter numéricos
    df["Temp. Ins. (C)"] = pd.to_numeric(df["Temp. Ins. (C)"], errors="coerce")
    df["Pressao Ins. (hPa)"] = pd.to_numeric(df["Pressao Ins. (hPa)"], errors="coerce")

    # Remover linhas vazias
    df = df.dropna(subset=["Data", "Temp. Ins. (C)", "Pressao Ins. (hPa)"])

    if df.empty:
        st.error("⚠ Não há dados válidos após conversão.")
        return

    df = df.set_index("Data")

    # Agrupar por dia
    df_diario = df.resample("D").mean()

    df_diario = df_diario.dropna()

    if df_diario.empty:
        st.error("⚠ Não há dados diários após agrupamento.")
        return

    st.subheader("📋 Dados Diários")
    st.dataframe(df_diario.head())

    dias = len(df_diario)
    passo = max(1, dias // 10)


    st.subheader("📈 Pressão Atmosférica por Dia")

    fig1, ax1 = plt.subplots(figsize=(12,5))
    ax1.plot(df_diario.index, df_diario["Pressao Ins. (hPa)"])
    ax1.set_ylabel("Pressão (hPa)")
    ax1.set_xlabel("Dia")

    ax1.set_xticks(df_diario.index[::passo])
    ax1.tick_params(axis="x", rotation=45)

    st.pyplot(fig1)


    st.subheader("🌡 Temperatura Média por Dia")

    fig2, ax2 = plt.subplots(figsize=(12,5))
    ax2.plot(df_diario.index, df_diario["Temp. Ins. (C)"])
    ax2.set_ylabel("Temperatura (°C)")
    ax2.set_xlabel("Dia")

    ax2.set_xticks(df_diario.index[::passo])
    ax2.tick_params(axis="x", rotation=45)

    st.pyplot(fig2)

    st.subheader("🔄 Relação Temperatura vs Pressão")

    fig3, ax3 = plt.subplots(figsize=(8,6))
    ax3.scatter(df_diario["Temp. Ins. (C)"],
                df_diario["Pressao Ins. (hPa)"])

    ax3.set_xlabel("Temperatura (°C)")
    ax3.set_ylabel("Pressão (hPa)")

    st.pyplot(fig3)


if __name__ == "__main__":
    dashboard_climatico()