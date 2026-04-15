import streamlit as st
import duckdb
import os
import configparser
from glob import glob
import pandas as pd

@st.cache_resource
def __conectar():
    return duckdb.connect(":memory:")

@st.cache_resource
def __obter_parquet_dir():
    prop_file = os.path.join(os.getcwd(), "config.ini")
    section_name = "EDUBASI"
    prop_name = "parquet_dir"
    if not os.path.exists(prop_file):
        print("Arquivo", prop_file, "não existe.")
        return None
        
    config = configparser.ConfigParser()
    config.read(prop_file, encoding="utf-8")
    if section_name not in config:
        print("Seção", section_name, "não encontrada.")
        return None

    if prop_name not in config[section_name]:
        print("Propriedade", prop_name, "não encontrada.")
        return None
    return config[section_name][prop_name]

def obter_dados(ano, id_municipio):
    id_sessao = ano + "_" + id_municipio
    if id_sessao in st.session_state:
        return st.session_state[id_sessao]
    parquet_dir = __obter_parquet_dir()
    parquet = os.path.join(parquet_dir, ano, f"{ano}_{id_municipio}.parquet")
    con = __conectar()
    df = con.execute(f"SELECT * FROM parquet_scan('{parquet}')").df()
    if str(ano) == '2018':
        df["TP_ESTADO_CIVIL"] = df["TP_ESTADO_CIVIL"].fillna("-1")
        df["TP_ESTADO_CIVIL"] = (df["TP_ESTADO_CIVIL"].astype(int) + 1).astype(str)
        df["TP_ESCOLA"] = df["TP_ESCOLA"].replace({3: 4, 4: 3})
        df["TP_PRESENCA_CN"] = df["TP_PRESENCA_CN"].replace({None: '0'})
        df["TP_PRESENCA_CH"] = df["TP_PRESENCA_CH"].replace({None: '0'})
        df["TP_PRESENCA_LC"] = df["TP_PRESENCA_LC"].replace({None: '0'})
        df["TP_PRESENCA_MT"] = df["TP_PRESENCA_MT"].replace({None: '0'})
    st.session_state[id_sessao] = df
    return st.session_state[id_sessao]

def iniciar_sessao():
    if "municipio_unico" not in st.session_state:
        st.session_state["municipio_unico"] = "1301902"
    if "municipios_multiplos" not in st.session_state:
        st.session_state["municipios_multiplos"] = []
    if "anos" not in st.session_state:
        #st.session_state["anos"] = obter_anos()
        st.session_state["anos"] = ['2018', '2022']

@st.cache_resource
def obter_municipios():
    df = pd.read_excel('municipios.xlsx', dtype=str)
    return df.set_index("NOME")["CODIGO"].to_dict()
    

@st.cache_resource
def obter_anos():
    parquet_dir = __obter_parquet_dir()
    anos = []
    for arq in glob(parquet_dir + "/*"):
        if os.path.isdir(arq):
            anos.append(os.path.basename(arq))
    return anos
    
def obter_municipio_selecionado():
    return st.session_state["municipio_unico"]

def selecionar_municipio(id_municipio):
    st.session_state["municipio_unico"] = id_municipio
    
def obter_municipios_selecionados():
    return st.session_state["municipios_multiplos"]

def selecionar_municipios(lista_municipios):
    st.session_state["municipios_multiplos"] = lista_municipios

def obter_anos_selecionados():
    return st.session_state["anos"]
    
def selecionar_anos(lista_anos):

    st.session_state["anos"] = lista_anos

