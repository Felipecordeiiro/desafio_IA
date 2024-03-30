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
                                dicionario[consulta] = [{key:value[posicao]} for key, value in dict_text.items() if value[posicao] != consulta]
        return dicionario

def specific_train(csvs_path, asks_specific, trainer_asks):

    for ask in asks_specific:
        for filename in csvs_path:
            try:
                trainer_asks.train([
                    asks_specific[ask].format(filename),
                    extrair_informacao(filename, ask),
                ])
            except:
                pass
    
def table_specific(csvs_path, asks_geral, trainer_asks):  
  
    for table in asks_geral:
        for filename in csvs_path:
            try:
                trainer_asks.train([
                    asks_geral[table].format(filename),
                    extrair_informacao(filename, table),
                ])
            except:
                pass

def geral_train(csvs_path, trainer_asks):

    for filename in csvs_path:
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

    asks_geral = {
        'Dados da Companhia': 'Quais os dados da companhia do {}?',
        'Balanço Patrimonial - Consolidado': 'Qual o balanço patrimonial do {}?',
        'Demonstração do Resultado - Consolidado': 'Qual o resultado do {}?',
        'Demonstração do Fluxo de Caixa - Consolidado': 'Qual o fluxo de caixa do {}?',
        'Posição Acionária*': 'Qual a posição acionária do {}?',
        'Ações em Circulação no Mercado': 'Quais as ações em circulação no mercado do {}?',
        'Composição do Capital Social': 'Qual a composição do capital social do {}?'
    }
    asks_specific = {
        'Nome de Pregão': 'Qual o nome de pregão do {}?',
        'Códigos de Negociação': 'Qual o códigos de negociação do {}?',
        'CNPJ': 'Qual o CNPJ do {}?',
        'Atividade Principal': 'Qual a atividade principal do {}?',
        'Classificação Setorial': 'Qual a classificação setorial do {}?',
        'Site': 'Qual o site do {}?',
        'Plantão de Notícias delay de 15 min.': 'Quais as noticias do {}?',
        'Ativo Imobilizado, Investimentos e Intangível': 'Qual é o ativo imobilizado do {}',
        'Ativo Total': 'Qual é o ativo total do {}',
        'Patrimônio Líquido': 'Qual é o patrimonio líquido do {}',
        'Patrimônio Líquido Atribuído à Controladora': 'Qual é o patrimonio líquido atribuido a controladora do {}',
        'Receita de Venda': 'Qual é a receita de venda do {}',
        'Resultado Bruto': 'Qual é o resultado bruto do {}',
        'Resultado de Equivalência Patrimonial': 'Qual é o resultado de equivalencia patrimonial do {}',
        'Resultado Financeiro': 'Qual é o resultado financeiro do {}',
        'Resultado Líquido das Operações Continuadas': 'Qual é o resultado líquido das operações continuadas do {}', 
        'Lucro (Prejuízo) do Período': '', 
        'Lucro (Prejuízo) do Período Atribuído à Controladora':'',
        'Atividades Operacionais': '', 
        'Atividades de Investimento': '', 
        'Atividades de Financiamento': '', 
        'Variação Cambial sobre Caixa e Equivalentes': '', 
        'Aumento (Redução) de Caixa e Equivalentes': '',
        'Pessoas Físicas': '',
        'Pessoas Jurídicas': '', 
        'Investidores Institucionais': '', 
        'Quantidade de Ações Ordinárias': '', 
        'Total de Ações':'',
    }

    csvs_list = os.listdir(csv_dir)
    csvs_paths = [os.path.join(csv_dir,csv_file) for csv_file in csvs_list if csv_file.endswith(".csv")]
    csvs_files = [csv_file.split(".")[0] for csv_file in csvs_list]       
    try:
        table_specific(csvs_paths, asks_geral, trainer_asks)
        specific_train(csvs_paths, asks_specific,trainer_asks)
        geral_train(csvs_paths, trainer_asks)
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
        "Perguntas gerais sobre um arquivo, como: {}".format(", ".join(asks_geral.values())),
        "Eu gostaria de ver as específicações",
        ", ".join(asks_specific.values())
    ])