import csv
import re
import ast
import pandas as pd

def extrair_informacao(arquivo_csv, consulta):
    df = pd.read_csv(arquivo_csv, encoding='utf-8')
    with open(arquivo_csv, encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        cabecalho = next(reader)  # Lê o cabeçalho
        informacoes = []
        # Encontra o índice da coluna correspondente à consulta
        indice_coluna = None
        for i, coluna in enumerate(cabecalho):
            if consulta.lower() in coluna.lower():
                print(df[consulta].values())
            else:
                for text in reader:
                    for information in text:
                        dict_info = ast.literal_eval(information)
                        for key, value in dict_info.items():
                            if consulta in key:
                                print(dict_info[consulta])
                                # Usa expressão regular para extrair o texto dentro das chaves
                                match = re.search(r'{([^}]*)}', dict_info[consulta])
                                if match:
                                    informacoes.append(match.group(1))
                            else:
                                pass

        
        if indice_coluna is None:
            return "Não foi possível encontrar informações para essa consulta."
        
        return informacoes

# Exemplo de uso:
arquivo_csv = 'csv-files\\abev3.csv'  # Substitua pelo caminho do seu arquivo CSV
consulta = 'Nome de Pregão'  # Consulta desejada

resultado = extrair_informacao(arquivo_csv, 'Dados da Companhia')
print(resultado)