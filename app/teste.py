

class Graficos:
    def __init__(self, dados):
        self.dados = dados
        self.colunas = ['NU_NOTA_CN', 'NU_NOTA_CH', 'NU_NOTA_LC', 'NU_NOTA_MT','NU_NOTA_REDACAO']
        self.colunas_nome = ['Ciências da Natureza', 'Ciências Humanas', 'Linguagens e Códigos', 'Matemática', 'Redação']
        for c in self.colunas:
            self.dados[c] = pd.to_numeric(self.dados[c], errors="coerce")
        self.anos = self.dados['NU_ANO'].unique()
    

    def porcentagem(self, parte, total):
        try:
            return ((parte / total) * 100) /100
        except ZeroDivisionError:
            return 0

    def gera_dataFreme_istograma_geral(self):
        notas = ['Sem nota','1-100', '101-200', '201-300', '301-400', '401-500', '501-600', '601-700', '701-800', '801-900', '901-1000']

        # Criar DataFrame para armazenar os resultados
        a = []
        for nota in notas:
            for _ in range(len(self.anos) +1):
                a.append(nota)
        df_medias = {'Faixa de Notas': a} 
        intervalos_notas = [None, (1,100), (101,200), (201,300), (301,400), (401,500), (501,600), (601,700), (701,800), (801,900), (901,1000)] 

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
                    qdt_alunos = len(df_ano[(df_ano >= intervalo[0]) & (df_ano <= intervalo[1])]) #qdt de alunos do ano em função da nota correspondente
                
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


   




    
    

    # --- Média das notas em barras interativo ---
    def media_das_notas(self):
        df_media = pd.DataFrame({
            'Disciplinas': self.colunas_nome,
            'Média das Notas': [
                round(self.dados["NU_NOTA_CN"].mean(), 4),
                round(self.dados["NU_NOTA_CH"].mean(), 4),
                round(self.dados["NU_NOTA_LC"].mean(), 4),
                round(self.dados["NU_NOTA_MT"].mean(), 4 ),
                round(self.dados["NU_NOTA_REDACAO"].mean(), 4)
            ]
        }).sort_values(by='Média das Notas', ascending=False)

        fig = px.bar(df_media,
                    x='Disciplinas',
                    y='Média das Notas',
                    
                    color_continuous_scale='blue',
                    labels={'Disciplinas': 'Disciplinas', 'Média das Notas': 'Média das Notas'},
                    title='  ')
        st.plotly_chart(fig, use_container_width=True)

    # --- Função que calcula faixa de notas (mantida igual) ---
    def sub_faixa_notas(self, coluna):
        df_faixa = pd.DataFrame({
            'Faixa de Notas': ['0-100', '101-200', '201-300', '301-400', '401-500', '501-600', '601-700', '701-800', '801-900', '901-1000'],
            'Quantidade de Alunos': [
                len(self.dados[(self.dados[coluna] >= 0) & (self.dados[coluna] <= 100)]),
                len(self.dados[(self.dados[coluna] > 100) & (self.dados[coluna] <= 200)]),
                len(self.dados[(self.dados[coluna] > 200) & (self.dados[coluna] <= 300)]),
                len(self.dados[(self.dados[coluna] > 300) & (self.dados[coluna] <= 400)]),
                len(self.dados[(self.dados[coluna] > 400) & (self.dados[coluna] <= 500)]),
                len(self.dados[(self.dados[coluna] > 500) & (self.dados[coluna] <= 600)]),
                len(self.dados[(self.dados[coluna] > 600) & (self.dados[coluna] <= 700)]),
                len(self.dados[(self.dados[coluna] > 700) & (self.dados[coluna] <= 800)]),
                len(self.dados[(self.dados[coluna] > 800) & (self.dados[coluna] <= 900)]),
                len(self.dados[(self.dados[coluna] > 900) & (self.dados[coluna] <= 1000)])
            ]
        })
        return df_faixa

    # --- Gráficos interativos de faixa de notas ---
    def faixa_notas(self):
        informacao = {
            'coluna_disciplina': ['NU_NOTA_CN', 'NU_NOTA_CH', 'NU_NOTA_LC', 'NU_NOTA_MT','NU_NOTA_REDACAO'],
            'lista_cores': ['blue', 'orange', 'green', 'red', 'purple'],
            'nomes_das_disciplinas': ['Ciências da Natureza', 'Ciências Humanas', 'Linguagens e Códigos', 'Matemática', 'Redação'],
            'eixoX': "Faixa de Notas",
            'eixoY': "Quantidade de Alunos"
        }

        for i in range(len(informacao['coluna_disciplina'])):
            with st.expander(f"Quantidade de Alunos por Faixa de Notas - {informacao['nomes_das_disciplinas'][i]}"):
                df_faixa = self.sub_faixa_notas(informacao['coluna_disciplina'][i])
                fig = px.bar(df_faixa,
                            x=informacao['eixoX'],
                            y=informacao['eixoY'],
                            color_discrete_sequence=[informacao['lista_cores'][i]],
                            labels={informacao['eixoX']: informacao['eixoX'], informacao['eixoY']: informacao['eixoY']},
                            title="  ")
                st.plotly_chart(fig, use_container_width=True)
    
    def calcular_medias_notas(self):


        lista_de_comparacao = [
            ['TX_RESPOSTAS_CN', 'TX_RESPOSTAS_CH', 'TX_RESPOSTAS_LC', 'TX_RESPOSTAS_MT'],
            ['TX_GABARITO_CN', 'TX_GABARITO_CH', 'TX_GABARITO_LC', 'TX_GABARITO_MT']
        ]

        lista_media_disciplinas_alunos = []
        for inde in range(len(lista_de_comparacao[0])):
            quantidade_alunos = 0
            dados = self.dados[[lista_de_comparacao[0][inde], lista_de_comparacao[1][inde]]].dropna().copy()
            quantidade_pontos = 0
            quantidade_questao = len(dados[lista_de_comparacao[0][inde]].iloc[0])
            for comparar in range(len(dados[lista_de_comparacao[0][inde]])):
                resposta_aluno = dados[lista_de_comparacao[0][inde]].iloc[comparar]
                gabarito = dados[lista_de_comparacao[1][inde]].iloc[comparar]
                tipo_lingua = False
                if (len(resposta_aluno) != len(gabarito)):
                    tipo_lingua = self.dados['TP_LINGUA'].iloc[comparar]
                quantidade_pontos += self.acertos_das_disciplinas(gabarito, resposta_aluno, tipo_lingua) 
                quantidade_alunos+=1

            
            #print(lista_de_comparacao[0][inde],'=> pontos', quantidade_pontos,'=> alunos', quantidade_alunos, '=> questoes', quantidade_questao )
            
            media = (quantidade_pontos/ quantidade_questao ) / quantidade_alunos
            media = float(f'{media: .9f}')
            lista_media_disciplinas_alunos.append(media)
        
        

        return lista_media_disciplinas_alunos


    def grafico_medias_das_notas_dos_alunos(self):
        data_freme = pd.DataFrame({
                'Disciplinas':self.colunas_nome[0:4],
                'Media': self.calcular_medias_notas()
            })
        fig = px.bar(
            data_freme,
            x='Disciplinas',
            y='Media',
            text='Media',
            labels={"Disciplinas":'Disciplinas' ,"Media":'Porcentagem nota'}
        )
        fig.update_traces(texttemplate="%{text:. 2f}%", textposition='outside')

        #update_traces(texttemplate='%{text:.1f}%', textposition='outside')

        st.plotly_chart(fig)

    
    def obter_dataFreme_ano(self, ano):
        qtd = 0
        aux = []
        for ano in edubasi.obter_anos_selecionados():
            st.write(ano)
            df = edubasi.obter_dados(ano = ano, id_municipio = edubasi.obter_municipio_selecionado())
            aux.append(df)
            qtd += len(df)

        df = pd.concat(aux, ignore_index=True, sort=False)
        st.write(df)

    
    def acertos_das_disciplinas(self, gabarito, resposta_aluno, tipo_ligua):
        if (not(tipo_ligua == False)):
            if (tipo_ligua == '0'):
                c = gabarito
                gabarito = gabarito[0:5]
                gabarito = gabarito + c[10:]
            else:
                gabarito = gabarito[5:]
            #print(gabarito)
        quantidade_pontos = 0
        for idece_resposta in range(len(gabarito)): # o ultimo aluno possui apenas 45 questões repondida sendo que o gabarito tem 50 então var ter indice do gabarito que não tem resposta
            if (resposta_aluno[idece_resposta] == gabarito[idece_resposta]):
                quantidade_pontos +=1
        return quantidade_pontos
    

    def sub_media_ano(self):
        disciplinas = self.colunas
        anos = self.anos

        matris = [
            [0 for _ in range(len(anos))] for _ in range(len(disciplinas))
        ]
      

        for l, disc in enumerate(disciplinas):
            for c, ano in enumerate(anos):
                df = self.dados[self.dados['NU_ANO'] == ano]
                media = df[disc].mean()
                matris[l][c] = round(media, 4)
        
        return matris
    

    def grafico_matris(self):

        disciplinas = self.colunas_nome
        anos = self.anos
        dados = self.sub_media_ano()
               
        df = pd.DataFrame(dados, index=disciplinas, columns=anos)

         # Cores fixas para os anos
        cores = ['blue', 'orange', 'green', 'red', 'purple']
        cores = cores[:len(anos)]

        fig = go.Figure()

        # Desenhar quadrados + adicionar texto
        for i, disc in enumerate(df.index):
            for j, ano in enumerate(df.columns):
                valor = df.loc[disc, ano]

                # Quadrado
                fig.add_shape(
                    type="rect",
                    x0=j, x1=j+1, y0=i, y1=i+1,
                    line=dict(color="black", width=1),
                    fillcolor=cores[j]
                )

                # Texto no centro
                fig.add_trace(go.Scatter(
                    x=[j+0.5], y=[i+0.5],
                    text=[str(valor)],
                    mode="text",
                    textfont=dict(color="white", size=14, family="Arial"),
                    hovertemplate=f"Disciplina: {disc}<br>Ano: {ano}<br>Média: {valor}<extra></extra>",
                    showlegend=False
                ))

        # Ajustar eixos
        fig.update_xaxes(
            tickvals=[j+0.5 for j in range(len(df.columns))],
            ticktext=list(df.columns),
            range=[0, len(df.columns)],
            title="Ano"
        )
        fig.update_yaxes(
            tickvals=[i+0.5 for i in range(len(df.index))],
            ticktext=list(df.index),
            range=[0, len(df.index)],
            title="Disciplina",
            autorange="reversed"
        )

        fig.update_layout(
            title="Médias por Disciplina e Ano",
            plot_bgcolor="white",
            margin=dict(l=40, r=40, t=60, b=40),
            height=400 + len(df.index) * 20  # ajusta tamanho automático
        )

        st.plotly_chart(fig, use_container_width=True)
  

