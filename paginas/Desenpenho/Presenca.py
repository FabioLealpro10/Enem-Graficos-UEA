

import streamlit as st
import pandas as pd
import plotly.express as px



class Presenca:
    def __init__(self, df):
        self.anos = df['NU_ANO'].unique() 
        self.cores_acerto_pesenca = ["rgb(200, 10, 58)", "rgb(109, 165, 87)"] # vermelho, verde

        st.subheader('Percentuais gerais em cada dia')
        nem_dia, dia1Apenas, dia2Apenas, todos_dias, total, dia1, dia2 =  self.levantar_dados(df)
        self.grafico1(nem_dia, dia1Apenas, dia2Apenas, todos_dias, total)
        st.subheader('Dia 1 - Linguagens e Códigos, Ciencias Humanas e Redação')
        

        coluna1, coluna2 = st.columns(2)
        with coluna1:
            self.grafico2(dia1, total, 'dia1', '')
        with coluna2:
            self.grafico3(df, ['TP_PRESENCA_LC', 'TP_PRESENCA_CH'], 'dia1_diferenca')
        with coluna1:
            self.grafico2(dia2, total, 'dia2', 'Dia 2 - Ciências da Naturesa e Matemática')
        with coluna2:
            self.grafico3(df, ['TP_PRESENCA_CN', 'TP_PRESENCA_MT'], 'dia2_diferenca')


    def levantar_dados(self, df):
        qdt_nem_um_dia = len(df[(df['TP_PRESENCA_CN']=='0') & (df['TP_PRESENCA_MT']=='0') & (df['TP_PRESENCA_CH']=='0') & (df['TP_PRESENCA_LC']=='0')])
        qdt_primeiro_dia = len(df[ (df['TP_PRESENCA_LC'].isin(('1', '2'))) & (df['TP_PRESENCA_CH'].isin(('1', '2')))])
        qdt_segundo_dia = len(df[(df['TP_PRESENCA_MT'].isin(('1', '2')) & (df['TP_PRESENCA_CN'].isin(('1', '2'))))])
        todos_os_dias =  len(df[(df['TP_PRESENCA_CH'].isin(('1', '2')) & (df['TP_PRESENCA_LC'].isin(('1', '2')))) & (df['TP_PRESENCA_CN'].isin(('1', '2'))) & (df['TP_PRESENCA_MT'].isin(('1', '2')))])


        qdt_primeiro_dia_apenas = qdt_primeiro_dia - todos_os_dias
        qdt_segundo_dia_apenas = qdt_segundo_dia - todos_os_dias

        total = qdt_nem_um_dia + qdt_primeiro_dia_apenas + qdt_segundo_dia_apenas + todos_os_dias
        return qdt_nem_um_dia, qdt_primeiro_dia_apenas, qdt_segundo_dia_apenas, todos_os_dias, total, qdt_primeiro_dia, qdt_segundo_dia,
    
    def grafico1(self, nem_dia, dia1, dia2, todos_dias, total):
        df = pd.DataFrame({
            'Categorias': ['Nem um dia', 'Apenas no 1º dia', 'Apenas no 2º dia', 'Ambos os dias'],
            'N° de Participantes': [nem_dia, dia1, dia2, todos_dias]
        })
        
        
        df['Percentual'] = (df['N° de Participantes'] / total).round(4)

        fig = px.bar(
            df,
            x="Categorias",
            y="Percentual",
            text=[f"{v*100:.2f}%" for v in df["Percentual"]],  # mostra texto no formato 0.00%
            color="Categorias",  # Usa a coluna de categorias para colorir
            color_discrete_sequence=[self.cores_acerto_pesenca[0], 'rgb(246, 207, 113)', 'rgb(248, 156, 116)', self.cores_acerto_pesenca[1]],
            hover_data=["N° de Participantes"]
        )

        fig.update_traces(
            textposition="inside",
            hovertemplate="%{x}<br>Percentual: %{y:.2%}<br>N° de Participantes: %{customdata[0]}<extra></extra>"
        )

        # Eixo Y com porcentagem de 0.00% até 100.00%
        fig.update_layout(
            yaxis=dict(
                title="Percentual",
                tickformat=".2%",  # <-- formato com 2 casas decimais
                range=[0, 1]       # 0 até 1 (representando 0% até 100%)
            ),
            xaxis_title="Categoria",
            showlegend=False
        )

        st.plotly_chart(fig, use_container_width=True)


    def grafico2(self, qdt_dia, total, nome, titulo):
        # 🔹 1. Criando um DataFrame de exemplo
        try:
            presentes = (qdt_dia * 100)/ total 
            ausentes = 100 - presentes
        except:
            presentes = 0
            ausentes = 0

        df = pd.DataFrame({
            "Categorias": ["Ausente", "Presente"],
            'percentual': [ausentes, presentes],
            "N° de Participantes": [total - qdt_dia, qdt_dia]
        })

        st.subheader(titulo)
        # 🔹 2. Criando o gráfico de pizza
        fig = px.pie(
            df,  # DataFrame com os dados
            names="Categorias",  # Coluna que define os rótulos (as fatias da pizza)
            values="N° de Participantes",  # Coluna com os valores (tamanho das fatias)
            color="Categorias",  # Define cores diferentes para cada categoria
            color_discrete_sequence=self.cores_acerto_pesenca,  # Define as cores das fatias
            hole=0.3,
            title="  "
        )

        # 🔹 3. Adicionando personalizações
        fig.update_traces(
            textinfo="percent+label",  # Mostra o nome da categoria + percentual
            textfont_size=16,  # Tamanho do texto nas fatias
            hoverinfo="label+value+percent"  # Mostra informações ao passar o mouse
        )

        # 🔹 4. Ajustando o layout do gráfico
        fig.update_layout(
            title_font_size=22,  # Tamanho do título
            legend_title_text="Categorias",  # Título da legenda
            legend_font_size=14,  # Tamanho do texto da legenda
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True, key=nome)

    def levantar_dados_ano(self, df, coluna_verificadas):
        qdt = []
        percentual_ano = []
        anos = []
        for ano in self.anos:
            df_ano = df[df['NU_ANO'] == ano]
            qdt_presente = len( df_ano[(df_ano[coluna_verificadas[0]].isin(('1', '2'))) & (df_ano[coluna_verificadas[0]].isin(('1', '2')))])
            qdt_total = len(df_ano)
            percentual = (qdt_presente * 100) / qdt_total
            percentual_ano.append(percentual)
            percentual_ano.append(100 - percentual)
            anos.append(ano)
            anos.append(ano)
            qdt.append(qdt_presente)
            qdt.append(qdt_total-qdt_presente)
        
        df_ano = df = pd.DataFrame({
            "Ano": anos,
            "Situação": ["Presentes", "Ausentes"]*len(self.anos),
            "Percentual": percentual_ano,
            'QDT. Participantes':qdt
        })

        return df_ano

    def grafico3(self, df, coluna_verificadas, diferenca):
        
        df = self.levantar_dados_ano(df, coluna_verificadas)

        #st.write(df)

        # 🔹 2. Criando o gráfico de barras empilhadas
        fig = px.bar(
            df,
            x="Ano",
            y="Percentual",
            color="Situação",
            text=df.apply(lambda row: f"{row['Percentual']:.2f}%", axis=1),
            custom_data=["Ano", "Percentual", "QDT. Participantes"],  # dados extras
            color_discrete_map={"Presentes":  self.cores_acerto_pesenca[1], "Ausentes": self.cores_acerto_pesenca[0]},
            barmode="relative",
            title="   "
        )

        # 🔹 3. Ajustes visuais
        fig.update_traces(
            textposition="inside",
            textfont_size=14,
            hovertemplate=
            "<b>Ano:</b> %{customdata[0]}<br>" +
            "<b>Percentual:</b> %{customdata[1]:.0f}%<br>" +
            "<b>QDT. Participantes:</b> %{customdata[2]}<extra></extra>"
        )

        # 🔹 4. Layout e estilo
        fig.update_layout(
            yaxis_title="Percentual (%)",
            xaxis_title=None,
            yaxis_range=[0, 100],  # Garante que a escala vá de 0 a 100%
            bargap=0.4,
            title_font_size=22,
            legend_title_text=None,
            legend_font_size=14
        )

        # 🔹 5. Exibir no Streamlit
        return st.plotly_chart(fig, use_container_width=True, key=diferenca)


