import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import configparser
from pathlib import Path
class MicroanaliseQuestoes:
    def __init__(self, anos, dados_aluno):
        
        self.anos = anos
        self.dados_aluno = dados_aluno

        self.dados = self.carregar_csv() # carrega os dados da prova


        self.sl_areas = self.dados['SG_AREA'].unique()
        self.area = ['Ciências da Natureza', 'Ciências Humanas', 'Linguagens e Códigos', 'Matemática']


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

        apenasQuestoesRespondida = st.checkbox("Deseja Analizar apenas as Questões que Foram Respondidas pelos alunos?", value=False) 

        self.dados_processados = self.acertos_por_habilidade_prova_especifica() # adiciona acertos por habilidade e codigos de provas diferentes
        
        self.Atribuir_acertos_as_questoes(apenasQuestoesRespondida) # adiciona acertos por questões de prova

        self.rum()
    


# carrega acertos por prova
        
    def encontrar_dados_prova(self):
        config = configparser.ConfigParser()
        config.read("config.ini")
        caminho = config.get("EDUBASI", "parquet_provas_questoes")

        return caminho

    
    def carregar_csv(self):
        dados = []
        caminhos = self.encontrar_dados_prova()
        for ano in self.anos:
            a = f'{caminhos}ITENS_PROVA_{ano}.csv' # caminho dos arquivos da prova
            df_ano = pd.read_csv(a, sep=';',  encoding='latin1')
            df_ano['ano'] = ano
            dados.append(df_ano)
        dados = pd.concat(dados, ignore_index=True)
        #dados = dados[dados['TX_MOTIVO_ABAN'].isna()] # remove as questões que foram anuladas



        return dados
    

    def carregar_csv_descricao_habilidade(self):
        caminho = Path(__file__).resolve().parents[2] / "habilidades.csv"
        carre_arquivo = pd.read_csv(caminho, sep=',',  encoding='utf-8')
        return carre_arquivo



    
# carrega acertos por prova



# carrega acertos por questões


    def sub_acerto_a_questao_especifica(self, indice_correto_questao_campara, codigo_prova, gabarito_questao_especifica, questão_aria):
        respostas_alunos = self.dados_aluno[(self.dados_aluno[f'CO_PROVA_{questão_aria}'] == codigo_prova)]
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
        return qdt_respostas_corretas, len(respostas_alunos) # retorna tambem as quantidade de acerto e quantos alunos responderam
    



    def Atribuir_acertos_as_questoes(self, apenasQuestoesRespondida):
        '''
            com os dados filtrados eu percorro eles tantando localizar todas as respostas daquele gabarito da quela prova
            fazer a contagem de acertos da quela intenciadade
            vou adicionar uma nova coluna no data freme de prova colocando a quantidade deacerto que a quela questão tenve dos alunos que fiseram a quela prova
            eu comparo os gabaritos e vou adicionando um em 1 para cada acerto e atualizando no data freme
            ate que todos os dados forem cotabilizados
        '''

        dados = self.dados['CO_PROVA'].unique()

        self.dados['QDT_ACERTOS_QUESTOES'] = None # quantidade de alunos que acertam a questão começa com vasio
        self.dados['QDT_ALUNOS_RESPONDERAM_QUESTAO'] = 0 # quantidade de alunos que respoderam a questão começando inicialmente com 0
        
        for cod_prova_especifica in dados: # percorre as provas
            Questoes_prova_especifica = self.dados[self.dados['CO_PROVA']== cod_prova_especifica] 
            for ln, questão_unica in Questoes_prova_especifica.iterrows(): # percorre as quesstois
                indice_correto_questao_campara = (questão_unica['CO_POSICAO'] % 45) - 1  # encontar o indece exato da questão para a comparação nas respostas 0 a 44
                codigo_prova = questão_unica['CO_PROVA']  
                gabarito_questao_especifica = questão_unica['TX_GABARITO']
                questão_aria = questão_unica['SG_AREA']
                acertos, qdt_alunos_responderam = self.sub_acerto_a_questao_especifica(indice_correto_questao_campara, 
                                                             str(codigo_prova), 
                                                             gabarito_questao_especifica,
                                                             questão_aria)
                
                self.dados.loc[ln, 'QDT_ACERTOS_QUESTOES'] = acertos #atribui a quantidade de acertos a linha da questão
                self.dados.loc[ln, 'QDT_ALUNOS_RESPONDERAM_QUESTAO'] = qdt_alunos_responderam #atribui a quantidade total de alunos que respoderam essa questão especifica
        if apenasQuestoesRespondida:
            # filtra e pega so as questões que foram respondidos 
            self.dados = self.dados[self.dados['QDT_ALUNOS_RESPONDERAM_QUESTAO']!=0] 
                

# carrega acertos por questões






# Quantidade de Questões por Área

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
        

#Quantidade de Questões por Área

    def tirar_porcentagem(self, qdt_parcela, qdt_total):
        try:
            return (qdt_parcela / qdt_total) * 100
        except:
            return 0






#Quantidades de questões por complexidade

    def criar_dataFreme_hitmap_facilidade_questoes(self, coluna, sg_complexidade):
        metricas_media = self.metricas_de_complexidade[coluna]
        percentua_metrica_chute = []

        # st.write('Maximo valor da',coluna, self.dados[sg_complexidade].max())
        # st.write('Minimo valor da',coluna, self.dados[sg_complexidade].min())

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
                disci_faci = {'aria': materia, 'Ano': ano, 'complexidade':'Baixa', 'Percentual':self.tirar_porcentagem(percemtual_chute_baixa, total)}
                disci_medi = {'aria': materia, 'Ano': ano, 'complexidade':'Média', 'Percentual':self.tirar_porcentagem(percemtual_chute_media, total) }
                disci_alta = {'aria': materia, 'Ano': ano, 'complexidade':'Alta', 'Percentual':self.tirar_porcentagem(percemtual_chute_alta, total)}
                percentua_metrica_chute.append(disci_faci)
                percentua_metrica_chute.append(disci_medi)
                percentua_metrica_chute.append(disci_alta)
        
            
            discri_facil_total = {'aria': 'Total', 'Ano': ano, 'complexidade':'Baixa', 'Percentual':self.tirar_porcentagem(soma_acertos_baixo, soma_total)}
            discri_medi_total = {'aria': 'Total', 'Ano': ano, 'complexidade':'Média', 'Percentual':self.tirar_porcentagem(soma_acertos_medio, soma_total)}
            discri_alta_total = {'aria': 'Total', 'Ano': ano, 'complexidade':'Alta', 'Percentual':self.tirar_porcentagem(soma_acertos_alto, soma_total)}
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


    def mostrar_analise_micro_dificuldade(self):
        with st.expander('Quantidades de questões por complexidade'):
            chute, difilcudade, discriminacao = st.tabs(['Facilidade de chute', 'Discriminação entre estudantes', 'Dificuldade de resolução'])
            with chute:
                self.apresentar_grafic_hitmap('Chute', 'NU_PARAM_C') # chute
            with difilcudade:
                self.apresentar_grafic_hitmap('Dificuldade', 'NU_PARAM_B') # dificuldade
            with discriminacao:
                self.apresentar_grafic_hitmap('Discriminação', 'NU_PARAM_A') # discriminação



#Quantidades de questões por complexidade




# carrega os acertos e das questões por prova especifica
    def sub_acertos_por_habilidade(self, df_questoes, df_resposta, area_prova):

        if len(df_resposta) == 0: # se niguem respondeu não contabiliza nada
            return None, None, 0, len(df_questoes)

        total_questoes = len(df_questoes) * len(df_resposta) # para cada aluno tem a mesma qdt de quesão pega o acumulado de questão
        total_acertos = 0 
        for li, resposta in df_resposta.iterrows():
            resposta_aluno = resposta[area_prova] 
            for questoes in df_questoes.itertuples():
                if resposta_aluno[(questoes.CO_POSICAO % 45) - 1] == questoes.TX_GABARITO:
                    total_acertos += 1
        return total_acertos, total_questoes, len(df_resposta), len(df_questoes)

    def acertos_por_habilidade_prova_especifica(self):
        #percorre disciplinas 
                #percorrer as provas de cada codigo
                    #percorre as habilidade
        diferentes_provas = self.dados['CO_PROVA'].unique() 
        habilidade_acertos = {'habilidade':[],
                             'CO_PROVA':[],
                             'QDT_ALUNOS_RESPONDIDO':[],
                             'QDT_ACERTOS':[],
                             'QDT_TOTAL_QUESTAO':[],
                             'ANO_PROVA':[],
                             'DISCIPLINA':[],
                             'QDT_EXATA_DE_QUESTOES_POR_HAB':[]
                             }
        
        # contabiliza dodos os dados da questões com os alunos
        for aria in self.sl_areas:
            co_prova_aria = f'CO_PROVA_{aria}'
            tx_resposta_aria = f'TX_RESPOSTAS_{aria}' 
            df_alunos = self.dados_aluno[[co_prova_aria, tx_resposta_aria ]].dropna()
            for habilidade in range(1, 31):
                df = self.dados[(self.dados['CO_HABILIDADE'] == habilidade)] 

                for prova in diferentes_provas:
                    prova_especifica =  df[df['CO_PROVA'] == prova][['CO_POSICAO', 'TX_GABARITO', 'ano']]

                    if not prova_especifica.empty: # tem algumas provas que não tem questões da habilidade especifica ex cod=>1105 na  habi=>7 não tem
                        ano = prova_especifica['ano'].iloc[0] 
                        prova_especifica_respondida = df_alunos[df_alunos[co_prova_aria]==str(prova)][[tx_resposta_aria]]
                        total_acertos, total_questoes, qdt_alunos_repondido, qdt_questao = self.sub_acertos_por_habilidade(prova_especifica, prova_especifica_respondida, tx_resposta_aria)
                        if qdt_alunos_repondido != 0:
                            # so adiciona no dataFre as questões que algun aluno respondeu
                            habilidade_acertos['habilidade'].append(habilidade)
                            habilidade_acertos['CO_PROVA'].append(prova)
                            habilidade_acertos['QDT_ACERTOS'].append(total_acertos)
                            habilidade_acertos['QDT_TOTAL_QUESTAO'].append(total_questoes)
                            habilidade_acertos['QDT_ALUNOS_RESPONDIDO'].append(qdt_alunos_repondido)
                            habilidade_acertos['ANO_PROVA'].append(ano)
                            habilidade_acertos['DISCIPLINA'].append(aria)
                            habilidade_acertos['QDT_EXATA_DE_QUESTOES_POR_HAB'].append(qdt_questao)

        habilidade_acertos = pd.DataFrame(habilidade_acertos)
        
        return habilidade_acertos

# carrega os acertos e das questões por prova especifica
        

            



#Quantidades de questões por habilidade


    def sub_apresentar_questões_habilidade(self, dados):

        colunas = ['Habilidade', 'Média'] + self.anos
       
        tabela = dados[colunas]

        tooltips = pd.DataFrame("", index=tabela.index, columns=tabela.columns)
        tooltips["Habilidade"] = dados["descricao"]

        styled = (
            tabela.style
                .hide(axis="index")
                .set_tooltips(tooltips)
                .set_table_attributes('style="width:100%"')  # 👈 força largura 100%
        )

        html = styled.to_html()

        st.markdown(html, unsafe_allow_html=True)
       


    def sub_questões_habilidade(self, aria):
        dados = self.dados_processados[(self.dados_processados['DISCIPLINA'] == aria) ]

        df_tipos_habilidade = self.carregar_csv_descricao_habilidade()

        dicionario_habilidade = {
            'CN':'Ciências da Natureza e suas Tecnologias',
            'CH':'Ciências Humanas e suas Tecnologias',
            'LC':'Linguagens, Códigos e suas Tecnologias',
            'MT':'Matemática e suas Tecnologias'
        }

        df_tipos_habilidade = df_tipos_habilidade[df_tipos_habilidade['Área'] == dicionario_habilidade[aria]]

        df = {'Habilidade':[],
              'Média':[],
              'descricao':[]
              }
        
        qdt = len(self.anos)
        for ano in self.anos:
            df[f'{ano}'] = []
        for hab in range(1, 31):
            df_habilidade = dados[dados['habilidade'] == hab]
            df['Habilidade'].append(f'Habilidade-{hab}') # nome da habilidade
            media_dos_anos = 0
            for ano in self.anos:
                df_ano = df_habilidade[df_habilidade['ANO_PROVA']== ano]
                media = df_ano['QDT_EXATA_DE_QUESTOES_POR_HAB'].mean()
                media = int(media) if not(pd.isna(media)) else 0
                df[f'{ano}'].append(media)
                media_dos_anos += media
            
            df['Média'].append(media_dos_anos//qdt )
            df['descricao'].append(f'Descrição da Habilidade-{hab}: {df_tipos_habilidade[df_tipos_habilidade['Código Habilidade']==f'H{hab}']['Descrição da Habilidade'].iloc[0]}')

        

        df = pd.DataFrame(df)
        
        self.sub_apresentar_questões_habilidade(df)
    
    def mostrar_habilidades(self):
        with st.expander('Quantidades de questões por habilidade'):
            CN, CH,LC, Ma = st.tabs(self.area)
            with CN:
                self.sub_questões_habilidade('CN')
            with CH:
                self.sub_questões_habilidade('CH')
            with LC:
                self.sub_questões_habilidade('LC')
            with Ma:
                self.sub_questões_habilidade('MT')


#Quantidades de questões por habilidade

                


#Habilidades de melhores desempenhos por área

    def sub_habilidades_aria(self, aria):
        dados = self.dados_processados[self.dados_processados['DISCIPLINA'] == aria] # pegar acertos por habilidade
        df_tipos_habilidade = self.carregar_csv_descricao_habilidade()

        dicionario_habilidade = {
            'CN':'Ciências da Natureza e suas Tecnologias',
            'CH':'Ciências Humanas e suas Tecnologias',
            'LC':'Linguagens, Códigos e suas Tecnologias',
            'MT':'Matemática e suas Tecnologias'
        }

        df_tipos_habilidade = df_tipos_habilidade[df_tipos_habilidade['Área'] == dicionario_habilidade[aria]]

        tabela = {
            'Habilidade':[],
            'Percentual de Acerto':[],
            'descricao':[]

        }

        for hab in range(1, 31):
            a = f'Habilidade - {hab}'
            df = dados[dados['habilidade'] == hab]
            if len(df) != 0: # Se houver dados para a habilidade
                qdt_acertos_habilidade = df['QDT_ACERTOS'].sum()
                qdt_total_questao_habilidade = df['QDT_TOTAL_QUESTAO'].sum()
                percentual = self.tirar_porcentagem(qdt_acertos_habilidade, qdt_total_questao_habilidade )
                tabela['Habilidade'].append(a)
                tabela['Percentual de Acerto'].append(percentual)
                tabela['descricao'].append(f'Descrição da Habilidade-{hab}: {df_tipos_habilidade[df_tipos_habilidade['Código Habilidade']==f'H{hab}']['Descrição da Habilidade'].iloc[0]}')
            
        tabela = pd.DataFrame(tabela)
        
        return tabela
    
    def sub_apresentar_tabela(self, dados, corDados):
        # Tabela que será exibida
        tabela = dados[['Habilidade', 'Percentual de Acerto']]

        # Criando dataframe de tooltips
        tooltips = pd.DataFrame("", index=tabela.index, columns=tabela.columns)
        tooltips["Habilidade"] = dados["descricao"]

        styled = (
            tabela.style.hide(axis="index")
                .format({"Percentual de Acerto": "{:.3f}%"})
                .background_gradient(
                    subset=["Percentual de Acerto"],
                    cmap=corDados,
                    vmin=0,
                    vmax=100
                )
                .set_tooltips(tooltips)
        )

        # ⚠️ MUITO IMPORTANTE
        html = styled.to_html(escape=False)

        # CSS separado (mais seguro)
        css = """
        <style>
        .tabela-container {
            width: 100% !important;
        }

        .tabela-container table {
            width: 100% !important;
            display: table !important;
        }
        </style>
        """

        st.markdown(css, unsafe_allow_html=True)

        st.markdown(
            f"""
            <div class="tabela-container">
                {html}
           
            """,
            unsafe_allow_html=True
        )
    def sub_Habilidades_desempenhos_por_area(self, dados_habilidade_CN, dados_habilidade_CH, dados_habilidade_LC, dados_habilidade_MT, cor, titulo):

         # opacidade das cores
        with st.expander(titulo):
            Cn, Ch,Lc, Ma = st.tabs(self.area)
        with Cn:
                self.sub_apresentar_tabela(dados_habilidade_CN, cor)
        with Ch:
                self.sub_apresentar_tabela(dados_habilidade_CH, cor)
        with Lc:
                self.sub_apresentar_tabela(dados_habilidade_LC, cor)
        with Ma:
               self.sub_apresentar_tabela(dados_habilidade_MT, cor)
    

    def Habilidade_desenpenho(self):
        mate = self.sub_habilidades_aria('MT')
        lingC = self.sub_habilidades_aria('LC')
        cienNat = self.sub_habilidades_aria('CN')
        cienHu = self.sub_habilidades_aria('CH')

        # 3 melhores
        dados_habilidade_CN = cienNat.nlargest(3, 'Percentual de Acerto')
        dados_habilidade_CH = cienHu.nlargest(3, 'Percentual de Acerto')
        dados_habilidade_LC = lingC.nlargest(3, 'Percentual de Acerto')
        dados_habilidade_MT = mate.nlargest(3, 'Percentual de Acerto')


        self.sub_Habilidades_desempenhos_por_area(dados_habilidade_CN, dados_habilidade_CH, dados_habilidade_LC, dados_habilidade_MT, 'Blues' ,'Habilidades de melhores desempenhos por área')

        # 3 piores
        dados_habilidade_CN = cienNat.nsmallest(3, 'Percentual de Acerto')
        dados_habilidade_CH = cienHu.nsmallest(3, 'Percentual de Acerto')
        dados_habilidade_LC = lingC.nsmallest(3, 'Percentual de Acerto')
        dados_habilidade_MT = mate.nsmallest(3, 'Percentual de Acerto')

        self.sub_Habilidades_desempenhos_por_area(dados_habilidade_CN, dados_habilidade_CH, dados_habilidade_LC, dados_habilidade_MT,'RdBu' ,'Habilidades de piores desempenhos por área')

#Habilidades de melhores desempenhos por área 







# Características dos acertos


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


    def preparar_dadosPercentual_de_acertoErro(self, E_acerto):
       
    # A - descriminação
    # B - dificuldade
    # C - acaso (chute)
       
       # Chute
       # baixa
       df = self.prepar_dados_acertos[self.prepar_dados_acertos['NU_PARAM_C']  < self.metricas_de_complexidade['Chute'][0]]
       qdt_acerto_chute_baixo = df['QDT_ACERTOS_QUESTOES'].sum() # soma tudo as questões acertadas com abaixo da metrica
       qdt_total_chute_baixo = df['QDT_ALUNOS_RESPONDERAM_QUESTAO'].sum() # soma tudo as questões respondidas com abaixo da metrica

       # média
       df = self.prepar_dados_acertos[(self.prepar_dados_acertos['NU_PARAM_C']  >= self.metricas_de_complexidade['Chute'][0]) 
                                               &
                                               (self.prepar_dados_acertos['NU_PARAM_C']  <= self.metricas_de_complexidade['Chute'][1])]
       qdt_acerto_chute_media = df['QDT_ACERTOS_QUESTOES'].sum()
       qdt_total_chute_media = df['QDT_ALUNOS_RESPONDERAM_QUESTAO'].sum() 

       # alta
       df = self.prepar_dados_acertos[self.prepar_dados_acertos['NU_PARAM_C']  > self.metricas_de_complexidade['Chute'][1]]
       qdt_acerto_chute_alta = df['QDT_ACERTOS_QUESTOES'].sum()
       qdt_total_chute_alta = df['QDT_ALUNOS_RESPONDERAM_QUESTAO'].sum()

       # Dificuldade
       # baixa
       df = self.prepar_dados_acertos[self.prepar_dados_acertos['NU_PARAM_B']  < self.metricas_de_complexidade['Dificuldade'][0]]
       qdt_acerto_dificuldade_baixo = df['QDT_ACERTOS_QUESTOES'].sum() 
       qdt_total_dificuldade_baixo = df['QDT_ALUNOS_RESPONDERAM_QUESTAO'].sum() 

       # média
       df = self.prepar_dados_acertos[(self.prepar_dados_acertos['NU_PARAM_B']  >= self.metricas_de_complexidade['Dificuldade'][0]) 
                                               &
                                               (self.prepar_dados_acertos['NU_PARAM_B']  <= self.metricas_de_complexidade['Dificuldade'][1])]
       qdt_acerto_dificuldade_media = df['QDT_ACERTOS_QUESTOES'].sum()
       qdt_total_dificuldade_media = df['QDT_ALUNOS_RESPONDERAM_QUESTAO'].sum()

       # alta
       df = self.prepar_dados_acertos[self.prepar_dados_acertos['NU_PARAM_B']  > self.metricas_de_complexidade['Dificuldade'][1]]
       qdt_acerto_dificuldade_alta = df['QDT_ACERTOS_QUESTOES'].sum()
       qdt_total_dificuldade_alta = df['QDT_ALUNOS_RESPONDERAM_QUESTAO'].sum()

       # Discriminação
       # baixa
       df = self.prepar_dados_acertos[self.prepar_dados_acertos['NU_PARAM_A']  < self.metricas_de_complexidade['Discriminação'][0]]
       qdt_acerto_discriminacao_baixo = df['QDT_ACERTOS_QUESTOES'].sum()
       qdt_total_discriminacao_baixo = df['QDT_ALUNOS_RESPONDERAM_QUESTAO'].sum()

        # média
       df = self.prepar_dados_acertos[(self.prepar_dados_acertos['NU_PARAM_A']  >= self.metricas_de_complexidade['Discriminação'][0]) 
                                               &
                                               (self.prepar_dados_acertos['NU_PARAM_A']  <= self.metricas_de_complexidade['Discriminação'][1])]
       qdt_acerto_discriminacao_media = df['QDT_ACERTOS_QUESTOES'].sum()
       qdt_total_discriminacao_media = df['QDT_ALUNOS_RESPONDERAM_QUESTAO'].sum()

       # alta
       df = self.prepar_dados_acertos[self.prepar_dados_acertos['NU_PARAM_A']  > self.metricas_de_complexidade['Discriminação'][1]]
       qdt_acerto_discriminacao_alta = df['QDT_ACERTOS_QUESTOES'].sum()
       qdt_total_discriminacao_alta = df['QDT_ALUNOS_RESPONDERAM_QUESTAO'].sum()

       if E_acerto: 
        # valores dos acertos
        df_vaolres = pd.DataFrame({
                'Parâmetro': ['Chute', 'Dificuldade', 'Discriminabilidade'],
                'Baixa': [qdt_acerto_chute_baixo, qdt_acerto_dificuldade_baixo, qdt_acerto_discriminacao_baixo],
                'Média': [qdt_acerto_chute_media, qdt_acerto_dificuldade_media, qdt_acerto_discriminacao_media],
                'Alta':  [qdt_acerto_chute_alta, qdt_acerto_dificuldade_alta, qdt_acerto_discriminacao_alta]
            })
       else:
           # valores dos erros 
           erros_baixo_chute =  qdt_total_chute_baixo - qdt_acerto_chute_baixo     
           erros_medio_chute = qdt_total_chute_media -  qdt_acerto_chute_media  
           erros_alto_chute = qdt_total_chute_alta - qdt_acerto_chute_alta


           erros_baixo_dificuldade =  qdt_total_dificuldade_baixo - qdt_acerto_dificuldade_baixo  
           erros_medio_dificuldade =  qdt_total_dificuldade_media - qdt_acerto_dificuldade_media
           erros_alto_dificuldade = qdt_total_dificuldade_alta - qdt_acerto_dificuldade_alta

           erros_baixo_descriminate = qdt_total_discriminacao_baixo -  qdt_acerto_discriminacao_baixo
           erros_medio_descriminate = qdt_total_discriminacao_media - qdt_acerto_discriminacao_media
           erros_alto_descriminate = qdt_total_discriminacao_alta - qdt_acerto_discriminacao_alta



           df_vaolres = pd.DataFrame({
                'Parâmetro': ['Chute', 'Dificuldade', 'Discriminabilidade'],
                'Baixa': [erros_baixo_chute,erros_baixo_dificuldade ,erros_baixo_descriminate ],
                'Média': [erros_medio_chute,erros_medio_dificuldade ,erros_medio_descriminate ],
                'Alta':  [erros_alto_chute,erros_alto_dificuldade , erros_alto_descriminate]
            })
           
       df_total = pd.DataFrame({
            'Parâmetro': ['Chute', 'Dificuldade', 'Discriminabilidade'],
            'Baixa': [qdt_total_chute_baixo, qdt_total_dificuldade_baixo, qdt_total_discriminacao_baixo],
            'Média': [qdt_total_chute_media,  qdt_total_dificuldade_media,  qdt_total_discriminacao_media],
            'Alta':  [ qdt_total_chute_alta,  qdt_total_dificuldade_alta,  qdt_total_discriminacao_alta]
        })
       
       return df_vaolres, df_total


    def Percentual_de_acertoErro_por_parâmetro_e_intensidade(self, Eacertos):
        df_acertos, df_total = self.preparar_dadosPercentual_de_acertoErro(Eacertos)

        if Eacertos: # configurações de graficos de acertos
            informacaoLabel = {
                "Parâmetro": "Parâmetro do Modelo TRI",
                "Percentual": "Percentual (%)",
                "Quantidade": "Quantidade Bruta",
                "Nível": "Nível"
            }
            cores = {
                "Baixa": "#35D3A1",  # verde
                "Média": "#3CD83F",  # laranja
                "Alta":  "#325199"   # azul
            }
            titulo = "Parâmetro de Intencidade do Modelo TRI de Acertos"
            informaValor =  "QDT.de alunos que acertaram/QDT.de alunos que Responderam"
        else: # configurações do grafico erro
            informacaoLabel = {
                "Parâmetro": "Parâmetro do Modelo TRI",
                "Percentual": "Percentual (%)",
                "Quantidade": "Quantidade Bruta",
                "Nível": "Nível"
            }
            cores = {
                "Baixa": "#C05841",  
                "Média": "#EE7D0C", 
                "Alta":  "#F4170B"   
            }
            titulo = "Parâmetro de Intencidade do Modelo TRI de Erros"
            informaValor =  "QDT.de alunos que Erraram/QDT.de alunos que Responderam"

        #  Mostrar tabelas (debug)
        # st.write(df_acertos)
        # st.write(df_total)

        #  Transformar em formato longo
        df_acertos_long = df_acertos.melt(
            id_vars='Parâmetro',
            var_name='Nível',
            value_name='Quantidade'
        )

        df_total_long = df_total.melt(
            id_vars='Parâmetro',
            var_name='Nível',
            value_name='Total'
        )

        #  Juntar os dois DataFrames corretamente (EVITA BUG)
        df_long = df_acertos_long.merge(
            df_total_long,
            on=['Parâmetro', 'Nível']
        )

        #  Calcular percentual corretamente
        df_long['Percentual'] = (df_long['Quantidade'] / df_long['Total']) * 100

        #  Criar gráfico
        fig = px.bar(
            df_long,
            x="Parâmetro",
            y="Percentual",
            color="Nível",
            barmode="group",
            text=df_long['Percentual'],  # usa o valor direto
            custom_data=["Quantidade", "Total"],
            labels=informacaoLabel,

            color_discrete_map=cores
        )

        #  Texto dentro da barra + hover
        fig.update_traces(
            texttemplate="%{y:.1f}%",
            textposition="inside",
            textfont_size=14,
            hovertemplate=(
                "Parâmetro: %{x}<br>"
                "Nível: %{fullData.name}<br>"
                "Percentual: %{y:.1f}%<br>"
                f"{informaValor}"+": %{customdata[0]} / %{customdata[1]}"
                "<extra></extra>"
            )
        )

        #  Layout
        fig.update_layout(
            title=" ",
            title_x=0.5,
            yaxis_title="Percentual (%)",
            xaxis_title=titulo,
            yaxis=dict(range=[0, 100]),
            bargap=0.2
        )

        #  Mostrar no Streamlit
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
        
    

    def caracteristicas_dos_acertosErros(self):
        with st.expander('Características dos acertos'):
            self.Distribuição_dos_acertos_por_parâmetro_e_intensidade()

            self.Percentual_de_acertoErro_por_parâmetro_e_intensidade(True) # grafico parametos acertos

            self.Percentual_de_acertoErro_por_parâmetro_e_intensidade(False) # grafico parametro de erro


            
            # self.curva_de_acertos('NU_PARAM_A','Percentual acumulado de acertos por intensidade de discriminação', self.dados)

            # self.curva_de_acertos('NU_PARAM_B','Percentual acumulado de acertos por intensidade de dificuldade', self.dados)
            
            # self.curva_de_acertos('NU_PARAM_C','Percentual acumulado de acertos por intensidade de chute', self.dados)

# Características dos acertos

    










    def rum(self):
        self.mostar_qdt_questao_area()
        self.mostrar_analise_micro_dificuldade()
        self.mostrar_habilidades()
        self.Habilidade_desenpenho()
        self.caracteristicas_dos_acertosErros()


        # carre_arquivo = pd.read_csv('/home/fabio-leal/Python/Enem-Graficos-UEA-main/microdados_enem_2024/DADOS/PARTICIPANTES_2024.csv', sep=';',  encoding='latin1').head(1)
        
        # carre_arquivo2 = pd.read_csv('/home/fabio-leal/Python/Enem-Graficos-UEA-main/microdados_enem_2024/DADOS/RESULTADOS_2024.csv', sep=';',  encoding='latin1').head(1)
        
        # st.write(carre_arquivo2.columns)
        # st.write(len(carre_arquivo2.columns))

        # st.write(carre_arquivo.columns)
        # st.write(len(carre_arquivo.columns))
        
        # st.write(self.dados_aluno.columns)
        # st.write(len(self.dados_aluno.columns))
        
        # #st.write(self.dados_processados)
        # # st.write(self.dados)
       
        # #st.write(self.dados[(self.dados['CO_PROVA'] == 465)])  

        # # # dados das respostas dos alunos
        # #st.write(self.dados_aluno[(self.dados_aluno['CO_PROVA_LC'] == '465')])


        


        

        

            

       

        
       
