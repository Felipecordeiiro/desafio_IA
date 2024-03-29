import os
import ast
import pandas as pd
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

def extrair_informacao(filename_csv, consulta=None):
    csv_dir = 'csv-files'
    csv_files = os.listdir(csv_dir)
    dicionario = {}

    # Tratamento do nome do arquivo
    if filename_csv.endswith(".csv"):
        pass
    else:
        filename_csv = filename_csv + '.csv'

    if filename_csv in csv_files:
        csv_files = [os.path.join(csv_dir, file) for file in csv_files if file.endswith(".csv")]
        for filepath in csv_files:
            filename = filepath.split("\\")
            if filename_csv == filename[1]:
                df = pd.read_csv(filepath, encoding='utf-8')
                cabecalho = list(df.columns)
                if consulta is None:
                    return df.to_dict()
                elif consulta in cabecalho:
                    return df[df.index == 0].values[0] #ast.literal_eval(df[consulta].values[0])
                else:
                    for i, text in df.items():
                        posicao = None
                        dict_text = eval(text[0])
                        for i, lista in enumerate(dict_text.values(), len(dict_text.keys())):
                            if consulta in lista:
                                posicao = lista.index(consulta)
                            elif posicao is not None:  # Verifica se posicao foi definida
                                dicionario[consulta] = [lista[posicao] for lista in dict_text.values() if lista[posicao] != consulta]
        return dicionario

def specific_train(csvs_list, trainer_asks):
    
    asks_specific = {
        'Nome de Pregão': 'Qual o nome de pregão do {}?',
        'Códigos de Negociação': 'Qual o códigos de negociação do {}?',
        'CNPJ': 'Qual o CNPJ do {}?',
        'Atividade Principal': 'Qual a atividade principal do {}?',
        'Classificação Setorial': 'Qual a classificação setorial do {}?',
        'Site': 'Qual o site do {}?',
        'Plantão de Notícias delay de 15 min.': 'Quais as noticias do {}?',
    }

    for ask in asks_specific:
        for filename in csvs_list:
            try:
                trainer_asks.train([
                    asks_specific[ask].format(filename),
                    extrair_informacao(filename, ask),
                ])
            except:
                pass
    
def table_specific(csvs_list, trainer_asks):  
    asks_geral = {
        'Dados da Companhia': 'Quais os dados da companhia do {}?',
        'Balanço Patrimonial - Consolidado': 'Qual o balanço patrimonial do {}?',
        'Demonstração do Resultado - Consolidado': 'Qual o resultado do {}?',
        'Demonstração do Fluxo de Caixa - Consolidado': 'Qual o fluxo de caixa do {}?',
        'Posição Acionária*': 'Qual a posição acionária do {}?',
        'Ações em Circulação no Mercado': 'Quais as ações em circulação no mercado do {}?',
        'Composição do Capital Social': 'Qual a composição do capital social do {}?'
    }
  
    for table in asks_geral:
        for filename in csvs_list:
            try:
                trainer_asks.train([
                    asks_geral[table].format(filename),
                    extrair_informacao(filename, table),
                ])
            except:
                pass

def geral_train(csvs_list, trainer_asks):

    for filename in csvs_list:
        try:
            trainer_asks.train([
                'Quais os dados gerais do {}'.format(filename),
                extrair_informacao(filename),
            ])
        except:
            pass


def train():
    csv_dir = "csv-files"

    chatbot = ChatBot(
        'Turing Bot',
        storage_adapter='chatterbot.storage.SQLStorageAdapter',
        database_uri='sqlite:///database.sqlite3'
    )

    trainer_asks = ListTrainer(chatbot)

    trainer_asks.train(
        "chatterbot.corpus.portuguese",
    )
    trainer_asks.train(
        "chatterbot.corpus.portuguese.greetings",
    )
    trainer_asks.train(
        "chatterbot.corpus.portuguese.conversations"
    )
    '''
    Pergunta[1]: Que informações disponíveis você tem sobre {Nome de Pregão}?
    Resposta[1]: Sobre qual exatamente você quer saber? Temos essas "asks_tables"
    Pergunta[2]: Sobre Dados da Companhia  
    Resposta[2]: ["'Nome de Pregão': 'AMBEV S/A', 'Códigos de Negociação': 'Mais Códigos', 'CNPJ': '07.526.557/0001-00', 'Atividade Principal': 'Fabricação E Distribuição de Cervejas. Refrigerantes E Bebidas Não Carbonatadas', 'Classificação Setorial': 'Consumo não Cíclico / Bebidas / Cervejas e Refrigerantes', 'Site': '', 'Plantão de Notícias delay de 15 min.': '11/03/2024 AMBEV S/A (ABEV) - Outros Comunicados ao Mercado - 11/03/24 08/03/2024 AMBEV S/A (ABEV) - VM Posicao Individual (Cia,Controladas e Coligadas)'"]
    Pergunta[3]: Me informe o "CNJP"
    Resposta[4]: 07.526.557/0001-00
    '''

    csvs_list = os.listdir(csv_dir)
    csvs_paths = [os.path.join(csv_dir,csv_file) for csv_file in csvs_list if csv_file.endswith(".csv")]
    csvs_files = [csv_file.split(".")[0] for csv_file in csvs_list]       
    for csv_file in csvs_paths:
        df = pd.read_csv(csv_file)
        try:
            table_specific()
            specific_train()
            geral_train()
        except:
                            pass
        except Exception as e:
            print(e)

    trainer_asks.train([
        "Quais são todos os relatórios que você tem informação?"
        '\n {}'.format(', '.join(csvs_files)),
    ])
    trainer_asks.train([
        "Ajuda",
        "Quer saber quais os tipos de perguntas disponíveis?",
        "Sim",
        "Perguntas gerais sobre um arquivo, como: {}".format(", ".join(asks_tables)),
        "Eu gostaria de ver as específicações",
        ", ".join(asks.values())
    ])