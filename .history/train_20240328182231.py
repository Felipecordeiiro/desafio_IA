import os
import csv
import re
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

def extrair_informacao(arquivo_csv, consulta):
    with open(arquivo_csv, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        cabecalho = next(reader)  # Lê o cabeçalho
        
        # Encontra o índice da coluna correspondente à consulta
        indice_coluna = None
        for i, coluna in enumerate(cabecalho):
            if consulta.lower() in coluna.lower():
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
        
        return informacoes

def train():
    csv_dir = "csv-files"

    chatbot = ChatBot(
        'Turing Bot',
        storage_adapter='chatterbot.storage.SQLStorageAdapter',
        database_uri='sqlite:///database.sqlite3'
    )

    trainer_asks = ListTrainer(chatbot)
    #Balanço Patrimonial - Consolidado,31/12/2023,31/12/2022,Demonstração do Resultado - Consolidado,01/01/2023 a 31/12/2023,01/01/2022 a 31/12/2022,Demonstração do Fluxo de Caixa - Consolidado,Nome,%ON,%PN,%Total,Tipos de Investidores / Ações,Quantidade,Percentual,Nomes,Valores

    asks = {
        'Empresa': 'Quando o relatório do {} foi atualizado?',
        'Códigos de Negociação': 'Qual o códigos de negociação do {}?',
        'CNPJ': 'Qual o CNPJ do {}?',
        'Atividade Principal': 'Qual a atividade principal do {}?',
        'Classificação Setorial': 'Qual a classificação setorial do {}?',
        'Site': 'Qual o site do {}?',
        'Plantão de Notícias delay de 15 min.': 'Quais as noticias do {}?',
        'Balanço Patrimonial - Consolidado': 'Qual o periodo do Balanço Patrimonial do {}?',
        'ativo_imobilizado': 'Qual é o ativo imobilizado do {}?',
        'ativo_total': 'Qual é o ativo total do {}?',
        'patrimonio_liquido': 'Qual é o pratimônio liquido do {}?',
        'patrimonio_liquido_controladora': 'Qual é o Patrimônio Líquido Atribuído à Controladora do {}?',
        'demonstracao_resultado': 'Quais os períodos da demonstração de resultados do {}?',
        'receita_de_venda': 'Qual é a Receita de Venda do {}?',
        'resultado_bruto': 'Qual é a Resultado Bruto do {}?',
        'resultado_de_equivalencia': 'Qual é o Resultado de Equivalência Patrimonial do {}?',
        'resultado_financeiro': 'Qual é a Resultado Financeiro do {}?',
        'resultado_liquido_continuado': 'Qual é a Resultado Líquido das Operações Continuadas do {}?',
        'lucro_prejuizo': 'Qual é o Lucro Prejuízo do Período do {}?',
        'lucro_prejuizo_controladora': 'Qual é o Lucro Prejuízo do Período Atribuído à Controladora do {}?',
        'demonstracao_fluxo_de_caixa': 'Qual é o período da Demonstração do Fluxo de Caixa do {}?',
        'atividades_operacionais': 'Quais é o valor das Atividades Operacionais do {}?',
        'atividades_de_investimento': 'Quais é o valor das Atividades de Investimento do {}?',
        'atividade_de_financiamento': 'Quais é o valor das Atividades de Financiamento do {}?',
        'avariacao_cambial': 'Quais é o valor das Variação Cambial sobre Caixa e Equivalentes do {}?',
        'aumento_reducao': 'Quais é o valor do Aumento (Redução) de Caixa e Equivalentes do {}?',
        'posicao_acionaria': 'Quais as Posições Acionárias do {}?',
        'informacoes_posicao_acionaria_recebida_em': 'Quando as posições acionárias do {} foram recebidas?',
        'acoes_em_circulacao_mercado': 'Quais as Ações em Circulação no Mercado do {}?',
        'composicao_capital_social': 'Qual a Composição do Capital Social do {}?'
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
    asks_company{
        ''
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
            for column in header:
                for information in column:
                    cod_list.append(information)
                    try:
                        trainer_asks.train([
                            trainer_asks.train([
                            information,
                            '\n'.join(extrair_informacao(os.path.join(csv_dir, csv_file_path), information)),
                        ])
                        ])
                    except Exception as e:
                        print(e)
                    break

    trainer_asks.train([
        "Quais são todos os códigos de negociação?",
        '\n'.join(cod_list),
    ])
    trainer_asks.train([
        "Ajuda",
        "Quer saber quais os tipos de perguntas disponíveis?",
        "Sim",
        '\n'.join(asks_tables)
    ])