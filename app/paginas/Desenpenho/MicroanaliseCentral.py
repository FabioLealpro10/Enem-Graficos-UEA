
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np


class MicroanaliseCentrais():
    def __init__(self, dados):
        self.dados = dados
        self.colunas = ['NU_NOTA_CN', 'NU_NOTA_CH', 'NU_NOTA_LC', 'NU_NOTA_MT','NU_NOTA_REDACAO']
        self.colunas_nome = ['Ciências da Natureza', 'Ciências Humanas', 'Linguagens e Códigos', 'Matemática', 'Redação']
        for c in self.colunas:
            self.dados[c] = pd.to_numeric(self.dados[c], errors="coerce")
        self.anos = self.dados['NU_ANO'].unique()

    def dados_iniciais_de_microanalise(self):

        dados = self.dados[self.colunas + ['NU_INSCRICAO']]
        local = dados.dropna(subset=self.colunas, how="any")
        
        local['media_geral'] = local[self.colunas].mean(axis=1, numeric_only=True) 

        
        media = round(local['media_geral'].mean(), 1)
        informacao = [media]
        for id, cod_disciplina in enumerate(self.colunas):
            local = dados.dropna(subset=cod_disciplina, how="any")
            media = local[cod_disciplina].mean()
            informacao.append(round(media, 1))
        

        colu1, colu2, colu3, colu4, colu5, colu6 = st.columns(6)
        with colu1:
            st.metric(label="Geral", value=informacao[0])
        with colu2:
            st.metric(label=self.colunas_nome[0], value=informacao[1])
        with colu3:
            st.metric(label=self.colunas_nome[1], value=informacao[2])
        with colu4:
            st.metric(label=self.colunas_nome[2], value=informacao[3])
        with colu5:
            st.metric(label=self.colunas_nome[3], value=informacao[4])
        with colu6:
            st.metric(label=self.colunas_nome[4], value=informacao[5])
    

    
    def criar_dataFreme_medias_matris(self, adm_escola, coluna):

        anos_selecionados = [f'Ano de {ano}' for ano in self.anos]
        anos_selecionados.append('Média Anual')
    
        matris_media_notas = []
        for linha, ano in enumerate(self.anos):
            df_ano = self.dados[self.dados['NU_ANO'] == ano]
            matris_media_notas.append([])
            for coluna_ano in range(len(adm_escola)):
                df_escola = df_ano[(df_ano[coluna] == str(coluna_ano + 1) if coluna_ano < (len(adm_escola) - 1) else df_ano[coluna].isna()) ]  
                df_escola = df_escola[self.colunas + [coluna]].dropna(subset=self.colunas, how="any") # remover linhas onde todas as colunas de notas são NaN
                df_escola['media_notas_adm_ano'] = df_escola[self.colunas].mean(axis=1, numeric_only=True)  
                df_escola = df_escola['media_notas_adm_ano'].mean()

                matris_media_notas[linha].append(0 if pd.isna(df_escola) else df_escola)
        
        matris_media_notas.append([])
        for id in range(len(matris_media_notas[0])):

            df_geral = self.dados[(self.dados[coluna] == str(id + 1) if id < (len(adm_escola) - 1) else self.dados[coluna].isna())]  
            df_geral = df_geral[self.colunas].dropna(subset=self.colunas, how="any") # remover linhas onde todas as colunas de notas são NaN
            df_geral['media_notas_adm_ano'] = df_geral[self.colunas].mean(axis=1, numeric_only=True)
            media = df_geral['media_notas_adm_ano'].mean()
            matris_media_notas[-1].append(media if not pd.isna(media) else 0)
        
        matris_media_notas = np.array(matris_media_notas)


        

        
        
        df = pd.DataFrame(matris_media_notas, index=anos_selecionados, columns=adm_escola)

        

        self.grafico_matris_adiministracao(df)
        

    def grafico_matris_adiministracao(self, df):
        # Garantir índices como texto
        df.index = df.index.astype("string")
        df.columns = df.columns.astype("string")

        fig = px.imshow(
            df.values,
            x=df.columns.tolist(),
            y=df.index.tolist(),
            labels=dict(x="Métrica", y="Ano", color="Nota"),
            color_continuous_scale=["white", "darkblue"],
            range_color=(0, 500),
            aspect="auto"
        )

        
        fig.data[0].text = df.values.astype(int)
        fig.update_traces(
            texttemplate="%{text}",
            textfont=dict(color="black", size=12)
        )

       
        fig.update_traces(
            customdata=df.values.reshape(df.shape[0], df.shape[1], 1),
            hovertemplate="Data: %{y}<br>Categoria: %{x}<br>Media Nota: %{customdata[0]:.2f}<extra></extra>"
        )

        fig.update_yaxes(autorange="reversed")
        fig.update_traces(textfont=dict(size=20))
        st.plotly_chart(fig, use_container_width=True)
        







            


    def gerar_medias_por_ano_e_disciplina(self):

        df_local = self.dados[self.colunas + ['NU_ANO']]
        df_local = df_local.dropna(subset=self.colunas, how="any") # remover linhas onde todas as colunas de notas são NaN
        df_medias = {}
        df_medias["Área"] = []
        df_medias['ano'] = []
        df_medias['Nota Media'] = []
        for id, disciplina in enumerate(self.colunas):
            
            for ano in self.anos:
                df_especifico = df_local[df_local['NU_ANO'] == ano]
                df_ano = df_especifico[disciplina].fillna(0)
                df_medias['Nota Media'].append(df_ano.mean())
                df_medias['Área'].append(self.colunas_nome[id])
                df_medias['ano'].append(ano)
            df = df_local[disciplina].fillna(0)
            df_medias['Nota Media'].append(df.mean())
            df_medias['Área'].append(self.colunas_nome[id])
            df_medias['ano'].append('Geral')
        
        df_medias = pd.DataFrame(df_medias)
        self.grafico_media_por_ano(df_medias)
    


    def grafico_media_por_ano(self, df_media):
        fig = px.bar(
            df_media,
            x="Área",
            y="Nota Media",
            color="ano",
            barmode="group",  # barras lado a lado
            text="Nota Media",  # mostra o valor dentro das barras
            custom_data=['ano'],
            labels={
                "Área": "Disciplinas",
                "Nota Media": "Média das Notas",
                "ano": "Ano",
            }
        )

        # Ajustar posição e estilo do texto
        fig.update_traces(
            texttemplate="%{text:.2f}",  # exibe valores com 2 casas decimais
            textposition="inside",
            textfont_size=14,
            hovertemplate="Disciplina: %{x}<br>Nota Média: %{y:.2f}<br>Ano: %{customdata[0]}<extra></extra>"
        )

        # Ajustar layout do eixo Y
        fig.update_layout(
            yaxis_title="Nota Média",
            xaxis_title="Disciplinas",
            yaxis=dict(
                range=[0, 1000]  # ajusta conforme a escala das suas notas
            ),
            title="Média de Notas por Área e Ano",
            title_x=0.5
        )

        # Mostrar no Streamlit
        st.plotly_chart(fig, use_container_width=True)
    


    def grafico_media_bloxoplot(self):
        dados = self.dados[self.colunas].dropna()
        dados.columns = self.colunas_nome
        dados = dados.melt(var_name="Disciplinas", value_name="Notas")
        fig = px.box(dados,
                    x= 'Disciplinas',
                    y='Notas',
                    color_discrete_sequence=px.colors.qualitative.Set3,
                    labels={c: c for c in dados.columns},
                    title=" ")
        
        st.plotly_chart(fig, use_container_width=True)
        
        



    def porcentagem(self, parte, total):
        try:
            return ((parte / total) * 100) /100
        except ZeroDivisionError:
            return 0

    def gera_dataFreme_istograma_geral(self):
        notas = ['Sem nota','1-100', '100-200', '200-300', '300-400', '400-500', '500-600', '600-700', '700-800', '800-900', '900-1000']

        # Criar DataFrame para armazenar os resultados
        a = []
        for nota in notas:
            for _ in range(len(self.anos) +1):
                a.append(nota)
        df_medias = {'Faixa de Notas': a} 
        intervalos_notas = [None, (1,100), (100,200), (200,300), (300,400), (400,500), (500,600), (600,700), (700,800), (800,900), (900,1000)] 

        df_medias['ano'] = []

        

        qdt_total_dados = len(self.dados)

        for ano in self.anos:
            df_medias['ano'].append(str(ano))
        df_medias['ano'].append("Geral")
        df_medias['ano'] = df_medias['ano'] * 11 

        df_medias['percentual'] = []
        df_medias['qdt_alunos'] = []


        for intervalo in intervalos_notas:
            qdt_total_aluno = 0
            
            for ano in self.anos:
                df_ano = self.dados[self.dados['NU_ANO'] == ano] # cria um dataframe para cada ano

                qdt_tota_ano = len(df_ano)
                
                df_ano = df_ano[self.colunas].fillna(0) # preencher valores NaN com 0 para cálculo da média
                df_ano = df_ano[self.colunas].mean(axis=1)
                if intervalo is None:
                    qdt_alunos = len(df_ano[df_ano == 0]) # qdt de alunos sem nota no ano
                else:
                    qdt_alunos = len(df_ano[(df_ano >= intervalo[0]) & (df_ano < intervalo[1])]) #qdt de alunos do ano em função da nota correspondente
                
                qdt_total_aluno += qdt_alunos
                percentual = round(self.porcentagem(qdt_alunos, qdt_tota_ano), 4)
        

                df_medias['qdt_alunos'].append(qdt_alunos) #qdt de alunos do ano em função da nota correspondente
                df_medias['percentual'].append(percentual) #percentual de alunos do ano em função da nota correspondente

            df_medias['qdt_alunos'].append(qdt_total_aluno) # soma qdt geral de alunos dos anos em função da nota correspondente 
            df_medias['percentual'].append(self.porcentagem(qdt_total_aluno, qdt_total_dados)) # soma o percentual media geral de alunos dos anos em função da nota correspondente 

        
        return pd.DataFrame(df_medias)
    

    def grafico_istograma_geral(self):
        df_medias = self.gera_dataFreme_istograma_geral()

        
        fig = px.bar(
            df_medias,
            x="Faixa de Notas",
            y="percentual",
            color="ano",
            barmode="group",  # barras lado a lado
            labels={
                "Faixa de Notas": "Faixa de Notas",
                "percentual": "Percentual de Estudantes",
                "ano": "Ano",
                "qdt_alunos": "Quantidade de Alunos"
            },
            text=[f"{v*100:.1f}%" for v in df_medias["percentual"]],  # mostra o valor como porcentagem
            hover_data=["qdt_alunos"]
        )

        # Ajustar posição e estilo do texto
        fig.update_traces(
            textposition="inside",
            textfont_size=20,
            hovertemplate="Faixa de Nota: %{x}<br>Percentual: %{y}<br>Quantidade de Alunos: %{customdata[0]}<extra></extra>"
        )

        # Ajustar layout do eixo Y e escala de porcentagem
        fig.update_layout(
            yaxis=dict(
                tickformat=".1%",  # exibe eixo Y como porcentagem
                range=[0, 0.5]    # limite até 35%
            )
        )

        # Mostrar no Streamlit
        st.plotly_chart(fig, use_container_width=True)
    

    def pagina_microalise_centrais(self):
        st.header("Média Aritmética")
        self.dados_iniciais_de_microanalise()

        with st.expander('Médias por ano e área'):
            self.gerar_medias_por_ano_e_disciplina()

        
        with st.expander("Histograma de médias gerais"):
            self.grafico_istograma_geral()

        with st.expander('Dispersão de notas'):
            self.grafico_media_bloxoplot()
        

        with st.expander('Médias por administração da escola'):
            self.criar_dataFreme_medias_matris(['Federal', 'Estadual', 'Municipal', 'Privada', 'Sem Informações'], 'TP_DEPENDENCIA_ADM_ESC')
        

        with st.expander('Médias por localidade da escola'):
            self.criar_dataFreme_medias_matris(['Urbana', 'Rural', 'Sem Informação'], 'TP_LOCALIZACAO_ESC')
        
        with st.expander('Médias por modalidade de ensino'):
            self.criar_dataFreme_medias_matris(['Ensino Regular', 'Educação Especial', 'Educação de Jovens e Adultos', 'Sem Informações'], 'TP_ENSINO')


