import streamlit as st
import pandas as pd
import plotly.express as px




class Incritos:
    def __init__(self, df):
        total, regulares, treneiros, ingles, espanhol =  self.valores(df)
        colu1, colu2, colu3, colu4, colu5 = st.columns(5)
        with colu1:
            st.metric(label="Total", value=total)
        with colu2:
            st.metric(label='Regulares', value=regulares)
        with colu3:
            st.metric(label='Treineiros', value=treneiros)
        with colu4:
            st.metric(label='Lingua inglesa', value=ingles)
        with colu5:
            st.metric(label='Lingua espanhola', value=espanhol)

        self.grafico_qdt_incritos_ano(df)
    
    def valores(self, df):
        total = len(df)
        qdt_treineiro = len(df[df['IN_TREINEIRO'] == '1'])
        qdt_regular = len(df[df['IN_TREINEIRO'] == '0'])
        qdt_ingles = len(df[df['TP_LINGUA'] == '0'])
        qdt_espanhol = len(df[df['TP_LINGUA'] == '1'])
        return total, qdt_regular, qdt_treineiro, qdt_ingles, qdt_espanhol 
    
    def grafico_qdt_incritos_ano(self, df):
        anos =  df['NU_ANO'].unique()
        valores = []
        for ano in anos:
            valores.append(len(df[df['NU_ANO'] == ano]))
        
        
        df = pd.DataFrame(
            {
                'Ano':anos,
                'Inscritos':valores
            }
        )
        grafico = px.bar(
            df,
            x='Ano',
            y='Inscritos',
            text='Inscritos',
            color='Ano',
            color_discrete_sequence=px.colors.qualitative.Pastel,
            title='Quantidade de Inscritos por ano'
        )
        grafico.update_traces(textposition='inside', textfont_size=20)
        grafico.update_layout(
            yaxis_title = 'Qdt. Inscritos',
            xaxis_title = 'Anos',
            bargap=0.6
        )
        st.plotly_chart(grafico, use_container_width=False)

