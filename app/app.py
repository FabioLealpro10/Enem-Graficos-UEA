import streamlit as st

from paginas import (
    municipios,
    enem_social,
    enem_desempenho,
    enem_comparativa,
    apagar # a ser apagada futuramente
)

st.set_page_config(page_title="Edubasi", layout="wide")

pg = st.navigation(
    {
        "": [
            st.Page(municipios.pagina_municipios, title="Escolha de municípios"),
        ],
        "ENEM": [
            st.Page(enem_social.pagina_enem_social, title="Social"),
            st.Page(enem_desempenho.pagina_enem_desempenho, title="Desempenho"),
            st.Page(enem_comparativa.pagina_enem_comparativa, title="Comparativa")
        ],
        "CENSO": [
            st.Page(apagar.pagina_apagar, title="A desenvolver") # a ser substituida
        ],
    }
)

pg.run()
