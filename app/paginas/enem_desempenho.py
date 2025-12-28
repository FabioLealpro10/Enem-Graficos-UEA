import streamlit as st
import pandas as pd
import edubasi


from .Desenpenho.Filtragem import Filtragem
from .Desenpenho.Inscritos import Incritos
from .Desenpenho.Presenca import Presenca
from .Desenpenho.MicroanaliseCentral import MicroanaliseCentrais
from .Desenpenho.MicroanalizeQuestoes import MicroanaliseQuestoes



def ordenar_anos(lista_anos):
    lista_anos = [int(ano) for ano in lista_anos]
    for cont in range(len(lista_anos)):
        for id in range(len(lista_anos) - (cont + 1)):
            if lista_anos[id] > lista_anos[id +1]:
                c = lista_anos[id]
                lista_anos[id] = lista_anos[id +1]
                lista_anos[id +1] = c
    lista_anos = [str(ano) for ano in lista_anos]
    return lista_anos
            


def filtra_inicial():
    qtd = 0
    aux = []
    anos = []
    for ano in edubasi.obter_anos_selecionados():
        anos.append(ano)
        df = edubasi.obter_dados(ano = ano, id_municipio = edubasi.obter_municipio_selecionado())

        aux.append(df)
        qtd += len(df)
    df = pd.concat(aux, ignore_index=True, sort=False)
    return df, anos



def pagina_enem_desempenho():
    edubasi.iniciar_sessao()
    df, data_anos = filtra_inicial()


    data_anos = ordenar_anos(data_anos)

    

    

     # --- SIDEBAR ---
    with st.sidebar:
        # --- GERAL ---
        with st.expander('Geral'):

            treineiro = st.checkbox('Incluir Estudantes Treineiros', value=True)
            studantes_sem_escola = st.checkbox("Incluir Estudantes sem Informações de Escola", value=True) 

            

            estado_civil = st.multiselect(
            "Selecione estado civil:",
            ["Solteiro", "Casado", "Divorciado", "Viúvo", 'Sem informação'],
            placeholder="Selecione estado civil:",

            )
            anos = st.multiselect(
            "Escolha os anos de análise:",
            data_anos,
            placeholder="Selecione os anos:",

            )
            sexo = st.radio("Filtragem por genero", ['Ambas pessoas', "Feminino", 'Masculino'])
        

            intervalo_idade =  st.slider(
                "Faixa etária de idade:",     
                min_value=0,          
                max_value=100,        
                value=(0, 100)       
            )


            
        with st.expander('Escola'):
        # --- ESCOLA ---

            tipo_escola = st.multiselect("Tipo de escola", ["Municipal", 'Estadual', 'Federal' , "Privada", 'Sem informação'], placeholder="Selecione o tipo de escola")


        # --- RENDA ---
        with st.expander('Renda'):
                        # --- MORADIA ---
            st.subheader("Moradia e Bens")

            empregados = st.multiselect("Filtro de estudantes que possuem empregado(a) doméstico(a).", 
                              ['Não Tem.',"Sim, um ou dois dias por semana.",
                                "Sim, três ou quatro dias por semana.",
                                "Sim, pelo menos cinco dias por semana."],
                                placeholder='Selecione os itens:')
            
            
            lista_itens = []
            for item in ['banheiro', 'quartos', 'carros', 'motocicleta', 'geladeira', 'freezer', 'máquina de lavar', 'máquina de secar roupa',
                        'micro-ondas', ' máquina de lavar louça', 'televisão em núcleos', 'telefone celular', ' computador']:
                item_sele = st.multiselect(f"Filtro por quantidade de {item} na residencia.", 
                                ['Não possui.',
                                "1",
                                "2",
                                "3",
                                '4 ou mais.'],
                                placeholder='Selecione os itens:')
                lista_itens.append(item_sele)
            
            
            inter = st.multiselect("Filtro por acesso a internet.", ["Possui internet", 'Não Possui internet'], placeholder="Selecione uma filtragem")
            renda = st.multiselect("Filtro de Renda familiar /salários mínimos", ['Nenhuma renda',
                                                                        'Até 1 salário mínimo',
                                                                        'Mais de 1 salário(s) até 1.5 salários',
                                                                        'Mais de 1.5 salário(s) até 2.0 salários',
                                                                        'Mais de 2.0 salário(s) até 2.5 salários',
                                                                        'Mais de 2.5 salário(s) até 3.0 salários',
                                                                        'Mais de 3.0 salário(s) até 4.0 salários',
                                                                        'Mais de 4.0 salário(s) até 5.0 salários',
                                                                        'Mais de 5.0 salário(s) até 6.0 salários',
                                                                        'Mais de 6.0 salário(s) até 7.0 salários',
                                                                        'Mais de 7.0 salário(s) até 8.0 salários',
                                                                        'Mais de 8.0 salário(s) até 9.0 salários',
                                                                        'Mais de 9.0 salário(s) até 10.0 salários',
                                                                        'Mais de 10.0 salário(s) até 12.0 salários',
                                                                        'Mais de 12.0 salário(s) até 15.0 salários',
                                                                        'Mais de 15.0 salário(s) até 20.0 salários',
                                                                        'Mais de 20 salários'
                                                                         ], placeholder="Selecione a renda familiar")


        # ainda fazer a filtragem por renda per capita

        # --- PROVA ---
        with st.expander('Prova'):
            # --- PROVA ---
            st.subheader("Prova")
            lingua = st.multiselect(
                "Filtragem por Língua estrangeira", 
                ["Inglês", "Espanhol"],
                placeholder="Selecione a língua estrangeira:"
            )
            



            presenca = st.multiselect(
                "Presença nas provas", 
                ["1º Dia (LC, CH, R)", "2º Dia (MT, CN)"],
                placeholder="Selecione a presença nas provas:"
            )
    
    anos = ordenar_anos(anos)
    ft = Filtragem()
    df = ft.filtra(estado_civil, intervalo_idade, tipo_escola, lingua, sexo, renda, presenca, anos, empregados,  lista_itens, inter, treineiro, studantes_sem_escola, df)
    st.title("Pespectiva de Desempenho")

    inscritos, presenca, macroanalise, microanalise = st.tabs(['Inscritos', 'Presença', 'Macroanálise', 'Microanálise'])

    with inscritos:
        Incritos(df)
    with presenca:
        Presenca(df)
    with macroanalise:
        macroanalise_questoes, macroanalise_centrais = st.tabs(['Macroanálise -> Questões', 'Macroanalize -> Centrais'])
        with macroanalise_questoes:
            if len(anos) == 0:
                anos = data_anos
            MicroanaliseQuestoes(anos, df)
            
        
        with macroanalise_centrais:
            MicroanaliseCentrais(df).pagina_microalise_centrais()
           

        


    

    


