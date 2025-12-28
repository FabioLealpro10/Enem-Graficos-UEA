
import pandas as pd




class Filtragem:
    def filtragem_por_estado_civil(self, estado_civil, df):
        if (len(estado_civil)>0): 
            filtrar_estado_civil = {
                "Solteiro": '0',
                "Casado":'1',
                "Divorciado": '2',
                "Viúvo":'3',
                'Sem informação': None
            }
            
            valores = [filtrar_estado_civil[x] for x in estado_civil]
            df = df[df['TP_ESTADO_CIVIL'].isin(valores)]
        return df
    

    def filtragem_por_idade(self, intervalo_idade, df):
        faxaIdade = {
            1:[0, 17],
            2:[17, 17],
            3:[18, 18],
            4:[19, 19],
            5:[20, 20],
            6:[21, 21],
            7:[22, 22],
            8:[23, 23],
            9:[24, 24],
            10:[25,25],
            11:[26,30],
            12:[31,35],
            13:[36,40],
            14:[41,45],
            15:[46,50],
            16:[51,55],
            17:[56,60],
            18:[61,65],
            19:[66,70],
            20:[71, 200]
        
        }
        faxaFiltrada = []
        for idice, valor in faxaIdade.items():
            if(intervalo_idade[0] <= valor[0] and  intervalo_idade[1] >= valor[1]):
                faxaFiltrada.append(idice)
        df['TP_FAIXA_ETARIA'] = pd.to_numeric(df['TP_FAIXA_ETARIA'], errors="coerce")
        
        df = df[df['TP_FAIXA_ETARIA'].isin(faxaFiltrada)]
        return df


    def filtragem_tipo_escola(self, tipo_escola, df):
        if (len(tipo_escola)>0): 
            filtrar_tipo_escola = {
            'Federal': '1',
            'Estadual': '2',        
            'Municipal': '3',
            'Privada': '4',
            'Sem informação':None
            }
            
            valores = [filtrar_tipo_escola[x] for x in tipo_escola]
            df = df[df['TP_DEPENDENCIA_ADM_ESC'].isin(valores)]
        return df


    def filtrar_lingua(self, lingua, df):
        if(len(lingua) != 0):
            filtrar_lingua = {
                "Inglês": '0',
                "Espanhol":'1'
            }
            
            valor = [filtrar_lingua[lingua] for lingua in lingua]
            df = df[df['TP_LINGUA'].isin(valor)]
        return df



    def filtar_ano(self, anos, df):
        if (len(anos)>0): 
            df = df[df['NU_ANO'].isin(anos)]
        return df
        


    def filtro_por_renda(self, df, renda):
        if (len(renda) > 0):
            dicionario = {
                    'Nenhuma Renda':'UM',	
                    'Até R$ 1.212,00':'B',
                    'De R$ 1.212,01 até R$ 1.818,00.':'C',
                    'De R$ 1.818,01 até R$ 2.424,00.':'D',
                    'De R$ 2.424,01 até R$ 3.030,00.':'E',
                    'De R$ 3.030,01 até R$ 3.636,00.':'F',
                    'De R$ 3.636,01 até R$ 4.848,00.':"G",
                    'De R$ 4.848,01 até R$ 6.060,00.':'H',
                    'De R$ 6.060,01 até R$ 7.272,00.':"EU",
                    'De R$ 7.272,01 até R$ 8.484,00.':"J",
                    'De R$ 8.484,01 até R$ 9.696,00.':"K",
                    'De R$ 9.696,01 até R$ 10.908,00.':"eu",
                    'De R$ 10.908,01 até R$ 12.120,00.':"M",
                    'De R$ 12.120,01 até R$ 14.544,00.':"N",
                    'De R$ 14.544,01 até R$ 18.180,00.':"O",
                    'De R$ 18.180,01 até R$ 24.240,00.':"P",
                    'Acima de R$ 24.240,00.':'P'
            }
            lista_renda = [dicionario[id] for id in renda]
            df = df[df['Q006'].isin(lista_renda)]
        return df


    def filtro_por_Pecapita(self, df, renda_pe):
        if (len(renda_pe) > 0):
            dicionario = {
          'Nenhuma renda':'A',
          'Até 1 salário mínimo':'B',
          'Mais de 1 salário(s) até 1.5 salários':'C',
          'Mais de 1.5 salário(s) até 2.0 salários':'D',
          'Mais de 2.0 salário(s) até 2.5 salários':'E',
          'Mais de 2.5 salário(s) até 3.0 salários':'F',
          'Mais de 3.0 salário(s) até 4.0 salários':'G',
          'Mais de 4.0 salário(s) até 5.0 salários':'H',
          'Mais de 5.0 salário(s) até 6.0 salários':'I',
          'Mais de 6.0 salário(s) até 7.0 salários':'J',
          'Mais de 7.0 salário(s) até 8.0 salários':'K',
          'Mais de 8.0 salário(s) até 9.0 salários':'L',
          'Mais de 9.0 salário(s) até 10.0 salários':'M',
          'Mais de 10.0 salário(s) até 12.0 salários':'N',
          'Mais de 12.0 salário(s) até 15.0 salários':'O',
          'Mais de 15.0 salário(s) até 20.0 salários':'P',
          'Mais de 20 salários':'Q'
            }
            lista_renda = [dicionario[id] for id in renda_pe]
            df = df[df['Q006'].isin(lista_renda)]
        return df

    def prenca_nas_provas(self, presenca, df):
        if (len(presenca) > 0 ):
            for valor in presenca:
                if ("1º Dia (LC, CH, R)" == valor):
                    df = df[(df['TP_PRESENCA_LC'].isin(('1', '2'))) & (df['TP_PRESENCA_CH'].isin(('1', '2')))]
                else:
                    df = df[(df['TP_PRESENCA_CN'].isin(('1', '2'))) & (df['TP_PRESENCA_MT'].isin(('1', '2')))]
        
        #consertar
        return df

    def filtragem_genero(self, sexo, df):
        filtrar_genero = {
            "Masculino": "M",
            "Feminino":"F"
        }
        if (sexo == 'Ambas pessoas'):
            return df
        valor = filtrar_genero[sexo]
        df = df[df['TP_SEXO'] == valor] 
        return df
    

    def filtrar_equipamento(self, lista_celecionados, df):
        dados = {
            'Não possui.':'UM',
            '1':'B',
            '2':'C',
            '3':'D',
            '4 ou mais.':'E',
        }
        coluna_verificar = ['Q008', 'Q009', 'Q010', 'Q011', 'Q012', 'Q013', 'Q014', 'Q015','Q016', 'Q017', 'Q019', 'Q022', 'Q024']
        for idice, item in enumerate(lista_celecionados):
            if (len(item) > 0 ):
                itens = [dados[x] for x in item]
                df = df[df[coluna_verificar[idice]].isin(itens)]

        return df
    
    def filtar_empregados(self, empregados, df):
        if (len(empregados) > 0 ):
            dados = {
                'Não Tem.':'UM',
                "Sim, um ou dois dias por semana.":'B',
                "Sim, três ou quatro dias por semana.":'C',
                "Sim, pelo menos cinco dias por semana.":'D'
            }
            
            itens = [dados[x] for x in empregados]
            df = df[df['Q007'].isin(itens)]
        return df
    
    def filtro_internete(self, inter, df):
        if (len(inter)!= 0):
            dados = {
            "Possui internet":'B',
            'Não Possui internet':'A'
            }
            inter = [dados[marcado] for marcado in inter]
            df = df[df['Q025'].isin(inter)]

                
        return df
    def filtro_treineiro(self, incluir_treineiro, df):
        if(not(incluir_treineiro)):
            df = df[df['IN_TREINEIRO'] == '0' ]
        
        return df
    
    def filtro_infor_escola(self, incluir, df):
        if(not(incluir)):
            df = df[df['TP_ESCOLA'] == '1']
        
        return df

    def filtra(self, estado_civil, intervalo_idade, tipo_escola, lingua, sexo, renda, presenca, anos, empregados, lista_celecionada, inter, treineiro, sem_escola, df ):
        
        df = self.filtragem_por_estado_civil(estado_civil, df)
        df = self.filtragem_por_idade(intervalo_idade, df)
        df = self.filtragem_tipo_escola(tipo_escola, df)
        df = self.filtrar_lingua(lingua, df)
        df = self.filtar_ano(anos, df)
        df = self.filtragem_genero(sexo, df)
        df = self.filtro_por_Pecapita(df, renda)
        df = self.prenca_nas_provas(presenca, df)
        df = self.filtar_empregados(empregados, df)
        df = self.filtrar_equipamento(lista_celecionada, df)
        df = self.filtro_internete(inter, df)
        df = self.filtro_treineiro(treineiro, df)
        df = self.filtro_infor_escola(sem_escola, df)
        return df
    
