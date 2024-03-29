import os
import csv
import re
import pandas as pd
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

def extrair_informacao(arquivo_csv, consulta, tabela=None):
    with open(arquivo_csv, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        cabecalho = next(reader)  # Lê o cabeçalho
        
        # Encontra o índice da coluna correspondente à consulta
        if tabela: 
            indice_coluna = None
            for i, coluna in enumerate(cabecalho):
                if tabela.lower() in coluna.lower():
                    indice_coluna = i
                    break
        
            if indice_coluna is None:
                return "Não foi possível encontrar informações para essa consulta."
        
            informacoes = []
            for linha in reader:
                celula = linha[indice_coluna]
                # Usa expressão regular para extrair o texto dentro das chaves
                match = re.search(r'{([^}]*)}', celula)
                if match:
                    informacoes.append(match.group(1))
            
            if not informacoes:
                return "Não foram encontradas informações para essa consulta."
        else:
            tabelas_disponiveis = []
            for coluna in cabecalho:
                if consulta.lower() in coluna.lower():
                    tabela = coluna.split(':')[0].strip()
                    tabelas_disponiveis.append(tabela)
            return tabelas_disponiveis

def empresas():


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

    asks_tables = {
        'Dados da Companhia',
        'Balanço Patrimonial - Consolidado',
        'Demonstração do Resultado - Consolidado',
        'Demonstração do Fluxo de Caixa - Consolidado',
        'Posição Acionária*',
        'Ações em Circulação no Mercado',
        'Composição do Capital Social'
    }
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
    column_list = []
    empresa_list = []
    for csv_file in csvs_list:
        df = pd.read_csv(csv_file)
        column_list = list(df.columns)
        filepath = os.path.join(csv_dir,csv_file)
        try:
            for column in column_list:
                trainer_asks.train([
                    column_list,
                    '\n'.join(extrair_informacao(filepath, column)),
                ])
        except Exception as e:
            print(e)
                    
    trainer_asks.train([
        "Quais são todas as empresas disponíveis?",
        '\n'.join(empresa_list),
        "Que informações disponíveis você tem sobre",
        '\n'.join(column_list)
    ])
    trainer_asks.train([
        "Ajuda",
        "Quer saber quais os tipos de perguntas disponíveis?",
        "Sim",
        "Informações gerais sobre um arquivo, como:{} E informações específicas, como: {}".join(asks_tables),
        "E informações específicas, como:",
        '\n'.join(asks)
    ])