
import streamlit as st
import pandas as pd

class MicroanaliseQuestoes:
    def __init__(self, anos, dados_aluno):
        
        self.anos = anos
        self.dados_aluno = dados_aluno
        self.dados = self.carregar_csv()
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

        self.rum()

    
    def carregar_csv(self):
        dados = []
        for ano in self.anos:
            a = f'/home/isack/Projeto 2025/Main/DadosProva/ITENS_PROVA_{ano}.csv'
            df_ano = pd.read_csv(a, sep=';',  encoding='latin1')
            df_ano['ano'] = ano
            dados.append(df_ano)
        dados = pd.concat(dados, ignore_index=True)
        return dados
    

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
                
                percemtual_chute_media = (len(discipli_filtrados[(discipli_filtrados[sg_complexidade] >= metricas_media[0]) & (discipli_filtrados[sg_complexidade] <= metricas_media[1])]))  # media
                soma_acertos_medio += percemtual_chute_media
                
                percemtual_chute_alta = (len(discipli_filtrados[discipli_filtrados[sg_complexidade] > metricas_media[1]]) )  # alta
                soma_acertos_alto += percemtual_chute_alta
                
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


    def acumular_acertos_habilidades(self, resposta, prova, ano, acertos_alunos_habilidade):
        dados_prova = self.dados[(self.dados['CO_PROVA'] == prova) & (self.dados['ano'] == ano)] # filtra o id da prova e o ano especifico
        dados_prova = dados_prova.itertuples(index=False) # gabarito sequencial
        # st.write(resposta)
        

        for id, questao in enumerate(dados_prova):
            if (questao.TX_GABARITO == resposta[id]) and (pd.isna(questao.TX_MOTIVO_ABAN)): # verifia a questão e se ela não foi anulada
                #st.write(questao.TX_GABARITO, resposta[id], questao.CO_HABILIDADE)
                acertos_alunos_habilidade[f'Habilidade {questao.CO_HABILIDADE}'] += 1 # acumula os acertos 
        
        return acertos_alunos_habilidade

        
    

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
            



    def Questoes_mais_acertadados_habilidade_CN(self):
        acertos_alunos_habilidade = {}
        for id in range(1, 31):
            acertos_alunos_habilidade[f'Habilidade {id}'] = 0

        dados_alunos = self.dados_aluno[['TX_RESPOSTAS_CN', 'CO_PROVA_CN']]
        dados_alunos = dados_alunos.dropna()

        dados_alunos = dados_alunos.itertuples(index=False)

        for ano in self.anos:
            for dado_alu in dados_alunos: 
                resposta_aluno =  dado_alu.TX_RESPOSTAS_CN
                cod_prova = int(dado_alu.CO_PROVA_CN)
                acertos_alunos_habilidade = self.acumular_acertos_habilidades(resposta_aluno, cod_prova, ano, acertos_alunos_habilidade)

        
        acertos_alunos_habilidade = self.ordenar_dicionario(acertos_alunos_habilidade)

        return acertos_alunos_habilidade













    def analizer_questoies_por_habilidade(self, aria):
        dados = self.dados[self.dados['SG_AREA'] == aria]
        dataFreme = {}
        dataFreme['Habilidade'] = []
        dataFreme['Média'] = []
        for ano in self.anos:
            dataFreme[f'{ano}'] = []

        for hab in range(1, 31):
            dataFreme['Habilidade'].append(f'Habilidade - H{hab}')
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

        
    
    def rum(self):
        self.mostar_qdt_questao_area()
        self.mostrar_analise_micro_dificuldade()
        self.mostrar_habilidades()
        st.write(self.Questoes_mais_acertadados_habilidade_CN())     
        


            

       

        
       


