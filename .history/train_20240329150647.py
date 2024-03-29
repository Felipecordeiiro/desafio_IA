import os
import ast
import pandas as pd
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

def extrair_informacao(filename_csv, consulta):
    csv_dir = 'csv-files'
    csv_files = os.listdir(csv_dir)

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

                if consulta in cabecalho:
                    return df[consulta].values
                else:
                    for i, text in df.iterrows():
                        dict_text = ast.literal_eval(text[i])
                        for key, value in dict_text.items():
                            if consulta in key:
                                return dict_text[consulta]
                            else:
                                pass

def train():
    csv_dir = "csv-files"

    chatbot = ChatBot(
        'Turing Bot',
        storage_adapter='chatterbot.storage.SQLStorageAdapter',
        database_uri='sqlite:///database.sqlite3'
    )

    trainer_asks = ListTrainer(chatbot)

    asks = {
        'Nome de Pregão': 'Qual o nome de pregão do {}?',
        'Códigos de Negociação': 'Qual o códigos de negociação do {}?',
        'CNPJ': 'Qual o CNPJ do {}?',
        'Atividade Principal': 'Qual a atividade principal do {}?',
        'Classificação Setorial': 'Qual a classificação setorial do {}?',
        'Site': 'Qual o site do {}?',
        'Plantão de Notícias delay de 15 min.': 'Quais as noticias do {}?',
    }

    asks_tables = [
        'Dados da Companhia',
        'Balanço Patrimonial - Consolidado',
        'Demonstração do Resultado - Consolidado',
        'Demonstração do Fluxo de Caixa - Consolidado',
        'Posição Acionária*',
        'Ações em Circulação no Mercado',
        'Composição do Capital Social'
    ]
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
    column_list = []
    for csv_file in csvs_paths:
        df = pd.read_csv(csv_file)
        column_list = list(df.columns)
        try:
            for column in column_list:
                for ask in asks:
                    print(ask)
                    for filename in csvs_list:
                        trainer_asks.train([
                            csvs_list,
                            column_list,
                            ask,
                            '\n'.join(extrair_informacao(filename, column)),
                        ])
        except Exception as e:
            print(e)

    trainer_asks.train([
        "Sobre qual relatório você quer saber?",
        '\n'.join(csvs_files),
        "Que informações disponíveis você tem sobre esse relatório?",
        '\n'.join(asks_tables)
    ])
    trainer_asks.train([
        "Ajuda",
        "Quer saber quais os tipos de perguntas disponíveis?",
        "Sim",
        "Perguntas gerais sobre um arquivo, como: {}".format(", ".join(asks_tables)),
        "Eu gostaria de ver as específicas",
        ", ".join(asks.values())
    ])