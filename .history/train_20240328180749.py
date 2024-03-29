import os
import csv
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

def train():
    csv_dir = "csv-files"

    chatbot = ChatBot(
        'Turing Bot',
        storage_adapter='chatterbot.storage.SQLStorageAdapter',
        database_uri='sqlite:///database.sqlite3'
    )

    trainer_asks = ListTrainer(chatbot)
    #Balanço Patrimonial - Consolidado,31/12/2023,31/12/2022,Demonstração do Resultado - Consolidado,01/01/2023 a 31/12/2023,01/01/2022 a 31/12/2022,Demonstração do Fluxo de Caixa - Consolidado,Nome,%ON,%PN,%Total,Tipos de Investidores / Ações,Quantidade,Percentual,Nomes,Valores
    '''
    '''
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

    csvs_list = os.listdir(csv_dir)
    cod_list = []

    for csv_file_path in csvs_list:
        with open(os.path.join(csv_dir, csv_file_path), 'r', encoding='UTF-8') as csv_file:
            reader = csv.reader(csv_file)
            header = next(reader)
            for csv_collumns in csv_data:
                print(csv_collumns)
                for csv_line in csv_collumns:
                    print(csv_line)
                    break
                    cod_list.append(csv_line['Nome de Pregão'])
                    for ask in asks:
                        print(ask)
                        try:
                            trainer_asks.train([
                                asks[ask].format(csv_line['Códigos de Negociação']),
                                csv_line[ask],
                            ])
                        except:
                            pass
                        break

    trainer_asks.train([
        "Quais são todos os códigos de negociação?",
        '\n'.join(cod_list),
    ])
    trainer_asks.train([
        "Ajuda",
        "Quer saber quais os tipos de perguntas disponíveis?",
        "Sim",
        '\n'.join(asks.values())
    ])