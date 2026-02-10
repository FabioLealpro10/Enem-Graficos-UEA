import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
import plotly.graph_objects as go

class MicroanaliseQuestoes:
    def __init__(self, anos, dados_aluno):
        
        self.anos = anos
        self.dados_aluno = dados_aluno
        self.dados = self.carregar_csv()
        self.sl_areas = self.dados['SG_AREA'].unique()
        self.area = ['Ciências da Natureza', 'Ciências Humanas', 'Linguagens e Códigos', 'Matemática']

        self.Atribuir_acertos_as_questoes()

        self.aria_co = {
            'CN':'Ciências da Natureza',
            'CH':'Ciências Humanas',
            'LC':'Linguagens e Códigos',
            'MT':'Matemática'
        }
        self.metricas_de_complexidade = {
            'Chute':[0.15, 0.20], # intervalo do meio de nivel de complexidade de chute
            'Dificuldade':[0.70, 1.5], # intervalo do meio de nivel de complexidade de dificuldade
            'Discriminação':[1.75, 2.5] # intervalo do meio de nivel de complexidade de discriminação
        }

        # essas variaves é para fazer a contagem das porcentagem no geral dos descriminates
        self.qdt_total_dos_descriminantes = {
            'Chute':[0, 0, 0], # idice 0 baixo, 1 medio, 2 alto
            'Dificuldade':[0, 0, 0],
            'Discriminação':[0, 0, 0],
        }

        self.rum()

    
    def carregar_csv(self):
        dados = []
        for ano in self.anos:
            a = f'/home/fabio-leal/Python/Enem-Graficos-UEA-main/dadosProva/ITENS_PROVA_{ano}.csv' # caminho dos arquivos da prova
            df_ano = pd.read_csv(a, sep=';',  encoding='latin1')
            df_ano['ano'] = ano
            dados.append(df_ano)
        dados = pd.concat(dados, ignore_index=True)
        dados = dados[dados['TX_MOTIVO_ABAN'].isna()] # remove as questões que foram anuladas


        return dados
    

    def atribuir_qdt_acerto_a_questao_especifica(self, indice_correto_questao_campara, codigo_prova, gabarito_questao_especifica, ano_questão, questão_aria):
        respostas_alunos = self.dados_aluno[(self.dados_aluno[f'CO_PROVA_{questão_aria}'] == codigo_prova) 
                                                                &    
                                                (self.dados_aluno['NU_ANO'] == ano_questão)]
        
       
        '''
            Essa filtagem seve para ter os dados apenas
            dos alunos que fizeram aquela questão especifica.
        '''
        
        qdt_respostas_corretas = 0 if len(respostas_alunos) > 0 else None 

        #st.write(respostas_alunos if len(respostas_alunos) > 0 else None  )
        '''
            alguns codigo de prova não possui no dataFreme dos alunos respondidos
            então não tem respostas para comparar a questão porisso retorna None.
        '''
        

        for ln, aluno in  respostas_alunos.iterrows():
            resposta_aluno = aluno[f'TX_RESPOSTAS_{questão_aria}']
            if resposta_aluno[indice_correto_questao_campara] == gabarito_questao_especifica: # compara se a reposta do aluno esta correta
                qdt_respostas_corretas +=1
            
            #st.write(resposta_aluno, resposta_aluno[indice_correto_questao_campara] == gabarito_questao_especifica, indice_correto_questao_campara, resposta_aluno[indice_correto_questao_campara], gabarito_questao_especifica, qdt_respostas_corretas)
  



        return qdt_respostas_corretas


        

    def Atribuir_acertos_as_questoes(self):
        '''
            com os dados filtrados eu percorro eles tantando localizar todas as respostas daquele gabarito da quela prova
            fazer a contagem de acertos da quela intenciadade
            vou adicionar uma nova coluna no data freme de prova colocando a quantidade deacerto que a quela questão tenve dos alunos que fiseram a quela prova
            eu comparo os gabaritos e vou adicionando um em 1 para cada acerto e atualizando no data freme
            ate que todos os dados forem cotabilizados
        '''

        dados = self.dados['CO_PROVA'].unique()

        self.dados['QDT_ACERTOS_QUESTOES'] = None # criar uma nova coluna com valores vazios
        for cod_prova_especifica in dados: # percorre as provas
            Questoes_prova_especifica = self.dados[self.dados['CO_PROVA']== cod_prova_especifica]
            questão_indice_maxima = Questoes_prova_especifica['CO_POSICAO'].max()   
            for ln, questão_unica in Questoes_prova_especifica.iterrows(): # percorre as quesstois
                indice_correto_questao_campara = 44 - (questão_indice_maxima - questão_unica['CO_POSICAO']) # encontar o indece exato da questão para a comparação nas respostas 0 a 44
                codigo_prova = questão_unica['CO_PROVA']  
                gabarito_questao_especifica = questão_unica['TX_GABARITO']
                ano_questão = questão_unica['ano']
                questão_aria = questão_unica['SG_AREA']
                acertos = self.atribuir_qdt_acerto_a_questao_especifica(indice_correto_questao_campara, 
                                                             str(codigo_prova), 
                                                             gabarito_questao_especifica,
                                                               ano_questão, questão_aria)
                
                self.dados.loc[ln, 'QDT_ACERTOS_QUESTOES'] = acertos #atribui a quantidade de acertos a linha da questão

    
        
        
    



    def qdt_questao_da_aria(self):
        tp_prova = self.dados['CO_PROVA'].unique()
        qdt_questao_area = {}
        for area in self.sl_areas:
            qdt_questao_area[area] = []
            for tp in tp_prova:
                qdt = len(self.dados[(self.dados['SG_AREA'] == area) & (self.dados['CO_PROVA'] == tp)])
                qdt_questao_area[area].append(qdt)

        # Criar DataFrame com ÁREAS como linhas e PROVAS como colunas
        qdt_questao_area = pd.DataFrame(qdt_questao_area, index=tp_prova).T
        #st.write(qdt_questao_area)

        # Criar dicionário final com valores únicos
        qdt_questao_area = {
            'CN': [qdt for qdt in qdt_questao_area.loc['CN'].unique() if qdt != 0][0], 
            'CH': [qdt for qdt in qdt_questao_area.loc['CH'].unique() if qdt != 0][0],
            'LC':int([qdt for qdt in qdt_questao_area.loc['LC'].unique() if qdt != 0][0]) - 5,
            'MT': [qdt for qdt in qdt_questao_area.loc['MT'].unique() if qdt != 0][0], 
        }
        return qdt_questao_area
    




    def criar_dataFreme_hitmap_facilidade_questoes(self, coluna, sg_complexidade):
        metricas_media = self.metricas_de_complexidade[coluna]
        percentua_metrica_chute = []
        for ano in self.anos:
            soma_acertos_baixo = 0
            soma_acertos_medio = 0
            soma_acertos_alto = 0
             
            ano_filtrado = self.dados[self.dados['ano'] == ano]
            soma_total = len(ano_filtrado)
            for disc in self.sl_areas:
                discipli_filtrados = ano_filtrado[ano_filtrado['SG_AREA'] == disc] 
                total = len(discipli_filtrados)
                
                percemtual_chute_baixa = (len(discipli_filtrados[discipli_filtrados[sg_complexidade] < metricas_media[0]]) ) # baixa
                soma_acertos_baixo += percemtual_chute_baixa
                self.qdt_total_dos_descriminantes[coluna][0] += percemtual_chute_baixa
                
                percemtual_chute_media = (len(discipli_filtrados[(discipli_filtrados[sg_complexidade] >= metricas_media[0]) & (discipli_filtrados[sg_complexidade] <= metricas_media[1])]))  # media
                soma_acertos_medio += percemtual_chute_media
                self.qdt_total_dos_descriminantes[coluna][1] += percemtual_chute_media
                
                percemtual_chute_alta = (len(discipli_filtrados[discipli_filtrados[sg_complexidade] > metricas_media[1]]) )  # alta
                soma_acertos_alto += percemtual_chute_alta
                self.qdt_total_dos_descriminantes[coluna][2] += percemtual_chute_alta
                

                
                materia = self.aria_co[disc]
                disci_faci = {'aria': materia, 'Ano': ano, 'complexidade':'Baixa', 'Percentual':(percemtual_chute_baixa / total) * 100}
                disci_medi = {'aria': materia, 'Ano': ano, 'complexidade':'Média', 'Percentual':(percemtual_chute_media / total) * 100}
                disci_alta = {'aria': materia, 'Ano': ano, 'complexidade':'Alta', 'Percentual':(percemtual_chute_alta/ total) * 100}
                percentua_metrica_chute.append(disci_faci)
                percentua_metrica_chute.append(disci_medi)
                percentua_metrica_chute.append(disci_alta)
        
            
            discri_facil_total = {'aria': 'Total', 'Ano': ano, 'complexidade':'Baixa', 'Percentual':(soma_acertos_baixo/soma_total) * 100}
            discri_medi_total = {'aria': 'Total', 'Ano': ano, 'complexidade':'Média', 'Percentual':(soma_acertos_medio/soma_total) * 100}
            discri_alta_total = {'aria': 'Total', 'Ano': ano, 'complexidade':'Alta', 'Percentual':(soma_acertos_alto/soma_total) * 100}
            percentua_metrica_chute.append(discri_facil_total)
            percentua_metrica_chute.append(discri_medi_total)
            percentua_metrica_chute.append(discri_alta_total)

        percentua_metrica_chute = pd.DataFrame(percentua_metrica_chute)
        percentua_metrica_chute.set_index("aria")
        percentua_metrica_chute = percentua_metrica_chute.pivot_table(
            index="aria",
            columns=["Ano", "complexidade"],
            values="Percentual",
        )
        percentua_metrica_chute.index.name = None
        return percentua_metrica_chute
    


    def apresentar_grafic_hitmap(self, categoria_questa, sg_complexidade):
        dados = self.criar_dataFreme_hitmap_facilidade_questoes(categoria_questa, sg_complexidade)
        st.dataframe(
            dados.style
                .format("{:.1f}%")
                .background_gradient(cmap="Blues")
        )


    
        
    




    def analizer_questoies_por_habilidade(self, aria):
        dados = self.dados[self.dados['SG_AREA'] == aria]
        dataFreme = {}
        dataFreme['Habilidade'] = []
        dataFreme['Média'] = []
        for ano in self.anos:
            dataFreme[f'{ano}'] = []

        for hab in range(1, 31):
            dataFreme['Habilidade'].append(f'Habilidade - {hab}')
            habilidade = dados[dados['CO_HABILIDADE'] == hab]
            soma = 0
            for ano in self.anos:
                ano_habilidade = habilidade[habilidade['ano'] == ano]
                quantidade = len(ano_habilidade)
                soma += quantidade
                dataFreme[ano].append(quantidade)
            dataFreme['Média'].append(int(soma/(len(self.anos))))
        
        dataFreme = pd.DataFrame(dataFreme)


        st.write(dataFreme) # apresenta os dados



        





    def mostar_qdt_questao_area(self):
        qdt_questoes_disc = self.qdt_questao_da_aria()
        with st.expander('Quantidade de Questões por Área'):
            colu1, colu2, colu3, colu4 = st.columns(4)
            with colu1:
                st.metric(label=self.area[0], value=qdt_questoes_disc['CN'])
            with colu2:
                st.metric(label=self.area[1], value=qdt_questoes_disc['CH'])
            with colu3:
                st.metric(label=self.area[2], value=qdt_questoes_disc['LC'])
            with colu4:
                st.metric(label=self.area[3], value=qdt_questoes_disc['MT'])
        


    def mostrar_analise_micro_dificuldade(self):
        with st.expander('Quantidades de questões por complexidade'):
            chute, difilcudade, discriminacao = st.tabs(['Facilidade de chute', 'Discriminação entre estudantes', 'Dificuldade de resolução'])
            with chute:
                self.apresentar_grafic_hitmap('Chute', 'NU_PARAM_C') # chute
            with difilcudade:
                self.apresentar_grafic_hitmap('Dificuldade', 'NU_PARAM_B') # dificuldade
            with discriminacao:
                self.apresentar_grafic_hitmap('Discriminação', 'NU_PARAM_A') # discriminação

    
    def mostrar_habilidades(self):
        with st.expander('Quantidades de questões por habilidade'):
            CN, CH,LC, Ma = st.tabs(self.area)
            with CN:
                self.analizer_questoies_por_habilidade('CN')
            with CH:
                self.analizer_questoies_por_habilidade('CH')
            with LC:
                self.analizer_questoies_por_habilidade('LC')
            with Ma:
                self.analizer_questoies_por_habilidade('MT')

    

    def menor_acerto_habilidade(self, discionario_desordenado):
        for id, valor in enumerate(discionario_desordenado.items()):
            if id == 0:
                idice = valor[0]
                menor = valor[1]
            else:
                if menor > valor[1]:
                    idice = valor[0]
                    menor = valor[1]
        return idice, menor


        
    def ordenar_dicionario(self, acertos_alunos_habilidade):
        dicionario_ordem = {}
        for id in range(1, 31):
            idice, valor = self.menor_acerto_habilidade(acertos_alunos_habilidade)
            del acertos_alunos_habilidade[idice]
            dicionario_ordem[idice] = valor
        return dicionario_ordem
        
    
    def dicionario_carrega_habilidade(self, aria):
        dados_habilidade = {}
        total = 0
        for habilidade in range(1, 31):
            df = self.dados[(self.dados['CO_HABILIDADE'] == habilidade) & (self.dados['SG_AREA']== aria)]
            todos_acertos = df['QDT_ACERTOS_QUESTOES'].sum()
            dados_habilidade[f'HABILIDADE: {habilidade}'] = todos_acertos
            total += todos_acertos
        dados_habilidade = self.ordenar_dicionario(dados_habilidade)

        return dados_habilidade, total
        


    
    def tabela_questoes_mas_acetadas(self, dados_originais, total): 
        dados = []
        for key, valores in reversed(list(dados_originais.items())[-3:]):
            dicio = {}
            dicio['Habilidade'] = key
            dicio['Quantidade de Acerto'] = valores
            dicio['Percentual de Acerto'] = (valores * 100) / total if total != 0 else 0
            dados.append(dicio)
        
        dados = pd.DataFrame(dados) # adicionar o sibolo da porcentagem %
        maior_valor = (max(dados_originais.values())* 100) / total
        menor_valor = (min(dados_originais.values())* 100) / total
        self.apresentar_tabela(dados, "Blues", menor_valor,  maior_valor)


    def apresentar_tabela(self, dados, corDados, menor, maior):
        #dados = dados[['Habilidade', 'Percentual de Acerto']] # pode apagar essa linha para aparecer todas as colunas de acetos
        
        st.dataframe(
            dados.style
                .format({"Percentual de Acerto": "{:.3f}%"})
                .background_gradient(
                    subset=["Percentual de Acerto"],
                    cmap=corDados,
                    vmin=menor,
                    vmax=maior
                )
        )

    
    


    def tabela_questoes_menos_acetadas(self, dados_originais, total):
        dados = []
        for key, valores in list(dados_originais.items())[:3]:
            dicio = {}
            dicio['Habilidade'] = key
            dicio['Quantidade de Acerto'] = valores
            dicio['Percentual de Acerto'] = (valores * 100) / total
            dados.append(dicio)
        
        dados = pd.DataFrame(dados) # adicionar o sibolo da porcentagem %

       
        maior_valor = (max(dados_originais.values())* 100) / total
        menor_valor = (min(dados_originais.values())* 100) / total
        self.apresentar_tabela(dados, "RdBu", menor_valor,  maior_valor)

    



    def Habilidades_de_melhores_desempenhos_por_aria(self, dados_habilidade_CN, total_CN,dados_habilidade_CH, total_CH, dados_habilidade_LC, total_LC, dados_habilidade_MT, total_MT):
        with st.expander('Habilidades de melhores desempenhos por área'):
            CN, CH,LC, Ma = st.tabs(self.area)
        with CN:
            self.tabela_questoes_mas_acetadas(dados_habilidade_CN, total_CN)
        with CH:
            self.tabela_questoes_mas_acetadas(dados_habilidade_CH, total_CH)
        with LC:
            self.tabela_questoes_mas_acetadas(dados_habilidade_LC, total_LC)
        with Ma:
            self.tabela_questoes_mas_acetadas(dados_habilidade_MT, total_MT)
    

    def Habilidades_de_piores_desempenhos_por_aria(self, dados_habilidade_CN, total_CN,dados_habilidade_CH, total_CH, dados_habilidade_LC, total_LC, dados_habilidade_MT, total_MT):
        with st.expander('Habilidades de piores desempenhos por área'):
            CN, CH,LC, Ma = st.tabs(self.area)
        with CN:
            self.tabela_questoes_menos_acetadas(dados_habilidade_CN, total_CN)
        with CH:
            self.tabela_questoes_menos_acetadas(dados_habilidade_CH, total_CH)
        with LC:
            self.tabela_questoes_menos_acetadas(dados_habilidade_LC, total_LC)
        with Ma:
            self.tabela_questoes_menos_acetadas(dados_habilidade_MT, total_MT)


    def Habilidades(self):
        dados_habilidade_CN, total_CN = self.dicionario_carrega_habilidade('CN')
        dados_habilidade_CH, total_CH = self.dicionario_carrega_habilidade('CH')
        dados_habilidade_LC, total_LC = self.dicionario_carrega_habilidade('LC')
        dados_habilidade_MT, total_MT = self.dicionario_carrega_habilidade('MT')
        self.Habilidades_de_melhores_desempenhos_por_aria(dados_habilidade_CN, total_CN, dados_habilidade_CH, total_CH, dados_habilidade_LC, total_LC, dados_habilidade_MT, total_MT)
        self.Habilidades_de_piores_desempenhos_por_aria(dados_habilidade_CN, total_CN,dados_habilidade_CH, total_CH, dados_habilidade_LC, total_LC, dados_habilidade_MT, total_MT)
        
    


    def apersentar_grafico_acertos_por_descriminante(self, qdt_acertos_de_descriminate_baixo, qdt_acertos_de_descriminate_medio, qdt_acertos_de_descriminate_alto, titulo):
      
        df = pd.DataFrame({
            'Nivel': ['Baixa', 'Média', 'Alta'],
            'Valor': [
                qdt_acertos_de_descriminate_baixo,
                qdt_acertos_de_descriminate_medio,
                qdt_acertos_de_descriminate_alto
            ]
        })

        # Mapa de cores por nível
        cores = {
            'Baixa': '#0D3B66',   # azul escuro
            'Média': '#4FC3F7',   # azul claro
            'Alta': '#D32F2F'     # vermelho
        }

        # Criar gráfico de pizza
        fig = px.pie(
            df,
            names='Nivel',
            values='Valor',
            title=titulo,
            hole=0,
            color='Nivel',
            color_discrete_map=cores
        )

        # Mostrar percentuais dentro do gráfico + hover customizado
        fig.update_traces(
            textinfo='percent',
            hovertemplate=(
                'Nível=%{label}<br>'
                'Percentual=%{percent}<br>'
                'Qtd de Acerto / Métrica de Complexidade=%{value}'
            )
        )

        # Exibir no Streamlit
        st.plotly_chart(fig)



    def prepara_dados(self, discriminate, coluna):
        intevalo_do_discriminante = self.metricas_de_complexidade [discriminate]

        dados = self.dados[self.dados['QDT_ACERTOS_QUESTOES'].notna()]# fazer um filtro para iginonar questoies que estão com acertos vasio
        
       

        qdt_acertos_de_descriminate_baixo = dados[dados[coluna] < intevalo_do_discriminante[0]]['QDT_ACERTOS_QUESTOES'].sum()

        #abaixo do intervalo
        qdt_acertos_de_descriminate_medio = dados[(dados[coluna] >= intevalo_do_discriminante[0])
                                                       & (dados[coluna] <= intevalo_do_discriminante[1])]['QDT_ACERTOS_QUESTOES'].sum()
        #entre o intervalo

        

        qdt_acertos_de_descriminate_alto = dados[dados[coluna]  > intevalo_do_discriminante[1]]['QDT_ACERTOS_QUESTOES'].sum()
        #superior ao intervalo

        self.prepar_dados_acertos = dados

        return qdt_acertos_de_descriminate_baixo, qdt_acertos_de_descriminate_medio, qdt_acertos_de_descriminate_alto









    
    def Distribuição_dos_acertos_por_parâmetro_e_intensidade(self):
        
        coluna_chute, coluna_dificuldade, coluna_descriminacao = st.columns(3)
        
        with coluna_chute:
            qdt_acertos_de_descriminate_baixo, qdt_acertos_de_descriminate_medio, qdt_acertos_de_descriminate_alto = self.prepara_dados('Chute', 'NU_PARAM_C')
            self.apersentar_grafico_acertos_por_descriminante(qdt_acertos_de_descriminate_baixo, qdt_acertos_de_descriminate_medio, qdt_acertos_de_descriminate_alto, 'Chute')
        
        with coluna_dificuldade:
            qdt_acertos_de_descriminate_baixo, qdt_acertos_de_descriminate_medio, qdt_acertos_de_descriminate_alto = self.prepara_dados('Dificuldade', 'NU_PARAM_B')
            self.apersentar_grafico_acertos_por_descriminante(qdt_acertos_de_descriminate_baixo, qdt_acertos_de_descriminate_medio, qdt_acertos_de_descriminate_alto, 'Dificuldade')

        with coluna_descriminacao:
            qdt_acertos_de_descriminate_baixo, qdt_acertos_de_descriminate_medio, qdt_acertos_de_descriminate_alto = self.prepara_dados('Discriminação', 'NU_PARAM_A')
            self.apersentar_grafico_acertos_por_descriminante(qdt_acertos_de_descriminate_baixo, qdt_acertos_de_descriminate_medio, qdt_acertos_de_descriminate_alto, 'Discriminação')


        
    
    def preparar_dadosPercentual_de_acerto(self):
       
    # A - descriminação
    # B - dificuldade
    # C - acaso (chute)
       
       chute_baixo = self.prepar_dados_acertos[self.prepar_dados_acertos['NU_PARAM_C']  < self.metricas_de_complexidade['Chute'][0]]['QDT_ACERTOS_QUESTOES'].sum()
       chute_media = self.prepar_dados_acertos[(self.prepar_dados_acertos['NU_PARAM_C']  >= self.metricas_de_complexidade['Chute'][0]) 
                                               &
                                               (self.prepar_dados_acertos['NU_PARAM_C']  <= self.metricas_de_complexidade['Chute'][1])]['QDT_ACERTOS_QUESTOES'].sum()
        
       chute_alta = self.prepar_dados_acertos[self.prepar_dados_acertos['NU_PARAM_C']  > self.metricas_de_complexidade['Chute'][1]]['QDT_ACERTOS_QUESTOES'].sum()


       dificuldade_baixo = self.prepar_dados_acertos[self.prepar_dados_acertos['NU_PARAM_B']  < self.metricas_de_complexidade['Dificuldade'][0]]['QDT_ACERTOS_QUESTOES'].sum()
       dificuldade_media = self.prepar_dados_acertos[(self.prepar_dados_acertos['NU_PARAM_B']  >= self.metricas_de_complexidade['Dificuldade'][0]) 
                                               &
                                               (self.prepar_dados_acertos['NU_PARAM_B']  <= self.metricas_de_complexidade['Dificuldade'][1])]['QDT_ACERTOS_QUESTOES'].sum()
        
       dificuldade_alta = self.prepar_dados_acertos[self.prepar_dados_acertos['NU_PARAM_B']  > self.metricas_de_complexidade['Dificuldade'][1]]['QDT_ACERTOS_QUESTOES'].sum()



       discriminacao_baixo = self.prepar_dados_acertos[self.prepar_dados_acertos['NU_PARAM_A']  < self.metricas_de_complexidade['Discriminação'][0]]['QDT_ACERTOS_QUESTOES'].sum()
       disccriminacao_media = self.prepar_dados_acertos[(self.prepar_dados_acertos['NU_PARAM_A']  >= self.metricas_de_complexidade['Discriminação'][0]) 
                                               &
                                               (self.prepar_dados_acertos['NU_PARAM_A']  <= self.metricas_de_complexidade['Discriminação'][1])]['QDT_ACERTOS_QUESTOES'].sum()
        
       discriminacao_alta = self.prepar_dados_acertos[self.prepar_dados_acertos['NU_PARAM_A']  > self.metricas_de_complexidade['Discriminação'][1]]['QDT_ACERTOS_QUESTOES'].sum()
       df = pd.DataFrame({
            'Parâmetro': ['Chute', 'Dificuldade', 'Discriminabilidade'],
            'Baixa': [chute_baixo, dificuldade_baixo, discriminacao_baixo],
            'Média': [chute_media, dificuldade_media, disccriminacao_media],
            'Alta':  [chute_alta, dificuldade_alta, discriminacao_alta]
        })
       
       return df


    def Percentual_de_acerto_por_parâmetro_e_intensidade(self):
        df = self.preparar_dadosPercentual_de_acerto()

        # deixa em percentual

        #st.write(df)

        colunas_nivel = ['Baixa', 'Média', 'Alta']

        # Criar DataFrame percentual
        df_percent = df.copy()
        total = df[colunas_nivel].sum(axis=1)
        df_percent[colunas_nivel] = df[colunas_nivel].div(total, axis=0) * 100

        # Converter para formato longo (manter bruto e %)
        df_long = df.melt(
            id_vars='Parâmetro',
            var_name='Nível',
            value_name='Quantidade'
        )

        df_percent_long = df_percent.melt(
            id_vars='Parâmetro',
            var_name='Nível',
            value_name='Percentual'
        )

        df_long['Percentual'] = df_percent_long['Percentual']

        # Criar gráfico
        fig = px.bar(
            df_long,
            x="Parâmetro",
            y="Percentual",
            color="Nível",
            barmode="group",
            text="Percentual",
            custom_data=["Quantidade"],
            labels={
                "Parâmetro": "Parâmetro do Modelo TRI",
                "Percentual": "Percentual (%)",
                "Quantidade": "Quantidade Bruta",
                "Nível": "Nível"
            },
            color_discrete_map={
                "Baixa": "#66C2A5",  # verde
                "Média": "#FC8D62",  # laranja
                "Alta":  "#8DA0CB"   # azul
            }
        )

        # Texto dentro da barra e hover
        fig.update_traces(
            texttemplate="%{text:.1f}%",
            textposition="inside",
            textfont_size=14,
            hovertemplate=(
                "Parâmetro: %{x}<br>"
                "Nível: %{fullData.name}<br>"
                "Percentual: %{y:.1f}%<br>"
                "QDT. acertos: %{customdata[0]}<extra></extra>"
            )
        )

        # Layout
        fig.update_layout(
            title=" ",
            title_x=0.5,
            yaxis_title="Percentual (%)",
            xaxis_title="Parâmetro do Modelo TRI",
            yaxis=dict(range=[0, 100])
        )

        # Mostrar no Streamlit
        st.plotly_chart(fig, use_container_width=True)


    

    def curva_de_acertos(self, parametro, titulo, df):
        df = df[[parametro, 'QDT_ACERTOS_QUESTOES']] 
        
        # Ordenar pelo parâmetro
        df = df.sort_values(by=parametro)

        # Percentual acumulado
        df["perc_acumulado"] = df["QDT_ACERTOS_QUESTOES"].cumsum() / df["QDT_ACERTOS_QUESTOES"].sum() * 100

        # Calcular AUC
        auc = np.trapezoid(df["perc_acumulado"], df[parametro])

        # Mostrar AUC
        st.metric("Área sob a curva", f"{auc:.3f}")

        # Criar gráfico de linha + área
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=df[parametro],
            y=df["perc_acumulado"],
            mode="lines+markers",
            fill="tozeroy",
            line=dict(width=3),
        ))

        fig.update_layout(
            title=titulo,
            xaxis_title="Valor da Discriminação",
            yaxis_title="Percentual acumulado (%)",
            yaxis=dict(range=[0, 100]),
        )

        st.plotly_chart(fig, use_container_width=True)
        #st.write(df)

        
        
        



    def rum(self):
        
        self.mostar_qdt_questao_area()
        self.mostrar_analise_micro_dificuldade()
        self.mostrar_habilidades()


        self.Habilidades()

        self.Distribuição_dos_acertos_por_parâmetro_e_intensidade()

        self.Percentual_de_acerto_por_parâmetro_e_intensidade()


        df = self.dados[self.dados['QDT_ACERTOS_QUESTOES'].notna()]
        self.curva_de_acertos('NU_PARAM_A','Percentual acumulado de acertos por intensidade de discriminação', df)

        self.curva_de_acertos('NU_PARAM_B','Percentual acumulado de acertos por intensidade de dificuldade', df)
        
        self.curva_de_acertos('NU_PARAM_C','Percentual acumulado de acertos por intensidade de chute', df)

        #st.write(self.dados[['NU_PARAM_A', 'QDT_ACERTOS_QUESTOES' ]])
        # st.write(self.dados_aluno[self.dados_aluno['CO_PROVA_LC'] == 496] )
        

        

            

       

        
       
