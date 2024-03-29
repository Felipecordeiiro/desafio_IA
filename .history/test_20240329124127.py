import csv
import re
import ast
import pandas as pd

def extrair_informacao(arquivo_csv, consulta):
    df = pd.read_csv(arquivo_csv, encoding='utf-8')
    cabecalho = list(df.columns)
    informacoes = []

    if consulta.lower() in coluna.lower():
        return df[consulta].values
    else:
        for text in reader:
            for information in text:
                dict_info = ast.literal_eval(information)
                for key, value in dict_info.items():
                    if consulta in key:
                        # Usa expressão regular para extrair o texto dentro das chaves
                        match = re.search(r'{([^}]*)}', dict_info[consulta])
                            if match:
                                informacoes.append(match.group(1))
                        else:
                            pass
        
        return informacoes

# Exemplo de uso:
arquivo_csv = 'csv-files\\abev3.csv'  # Substitua pelo caminho do seu arquivo CSV
consulta = 'Nome de Pregão'  # Consulta desejada

resultado = extrair_informacao(arquivo_csv, 'Dados da Companhia')
print(resultado)