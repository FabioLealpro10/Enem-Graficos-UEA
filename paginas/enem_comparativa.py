import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import edubasi
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import edubasi

def pagina_enem_comparativa():
    edubasi.iniciar_sessao()
    
    st.title("Perspectiva de Comparativa")

    estado_civil = st.sidebar.multiselect(
        "Selecione estado civil:",
        ["Solteiro", "Casado", "Divorciado", "Viúvo"],
        placeholder="Selecione um município"
    )
    qtd = 0
    aux = []
    for ano in edubasi.obter_anos_selecionados():
        st.write(ano)
        df = edubasi.obter_dados(ano = ano, id_municipio = edubasi.obter_municipio_selecionado())
        aux.append(df)
        qtd += len(df)

    df = pd.concat(aux, ignore_index=True, sort=False)
    
    st.write("Município único selecionado:", edubasi.obter_municipio_selecionado())
    st.write("Municípios múltiplos selecionados:", edubasi.obter_municipios_selecionados())
    st.write("Quantidade de registros: " + str(qtd))
    st.write(df)


    df = pd.DataFrame({"Categoria": ["A", "B", "C", "D"], "Valor": [10, 20, 15, 30]})

    fig1, ax1 = plt.subplots()
    ax1.bar(df["Categoria"], df["Valor"])
    ax1.set_title("Gráfico de Barras 1")
    st.pyplot(fig1)

    fig2, ax2 = plt.subplots()
    ax2.bar(df["Categoria"], df["Valor"], color="orange")
    ax2.set_title("Gráfico de Barras 2")
    st.pyplot(fig2)
