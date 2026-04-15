import streamlit as st
import edubasi
import pandas as pd

def pagina_municipios():
    st.title("Seleção de Municípios e Anos")
    
    edubasi.iniciar_sessao()
    
    lista_municipios = edubasi.obter_municipios()
    lista_anos = edubasi.obter_anos()

    nome_municipio_unico = st.selectbox(
        "Escolha um município:",
        options=list(lista_municipios.keys()),
        index=list(lista_municipios.values()).index(edubasi.obter_municipio_selecionado())
    )
    id_municipio_unico = lista_municipios[nome_municipio_unico]

    nomes_municipios_multiplos = st.multiselect(
        "Escolha até 4 municípios:",
        options=list(lista_municipios.keys()),
        default=[nome for nome, id_ in lista_municipios.items() if id_ in edubasi.obter_municipios_selecionados()],
        max_selections=4,
        placeholder="Selecione outros municípios (opcional)"
    )
    ids_municipios_multiplos = [lista_municipios[nome] for nome in nomes_municipios_multiplos]
    
    anos = st.multiselect(
        "Escolha os anos de análise:",
        lista_anos,
        default=edubasi.obter_anos_selecionados(),
        placeholder="Selecione ao menos um ano"
    )
    
    
    if st.button("Atualizar"):
        if len(anos) == 0:
            st.warning("Escolha, pelo menos, um ano de análise.")
        else:
            edubasi.selecionar_municipio(id_municipio_unico)
            edubasi.selecionar_municipios(ids_municipios_multiplos)
            edubasi.selecionar_anos(anos)
            st.success("Municípios e anos confirmados e salvos!")
