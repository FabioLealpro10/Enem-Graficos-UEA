import streamlit as st

from paginas import apagar



def cabecalho():
    col1, col2 = st.columns([1, 9])
    with col1:
        st.image("logo.png", width=90)
    with col2:
        st.title("Edubasi Painel")

    
    

from paginas import (
    municipios,
    enem_social,
    enem_desempenho,
    enem_comparativa
)


cabecalho()
pg = st.navigation(
    {
        "": [
            st.Page(municipios.pagina_municipios, title="Escolha de municípios"),
        ],
        "ENEM": [
            st.Page(enem_social.pagina_enem_social, title="Social"),
            st.Page(enem_desempenho.pagina_enem_desempenho, title="🧠 Perspectiva de Desempenho"),
            st.Page(enem_comparativa.pagina_enem_comparativa, title="Comparativa")
        ],
        "CENSO": [
            st.Page(apagar.pagina_apagar, title="A desenvolver")
        ],
    }
)

pg.run()