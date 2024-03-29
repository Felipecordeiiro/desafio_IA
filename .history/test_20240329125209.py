import csv
import re
import ast
import pandas as pd

def extrair_informacao(arquivo_csv, consulta):
    df = pd.read_csv(arquivo_csv, encoding='utf-8')
    cabecalho = list(df.columns)
    informacoes = []

    if consulta in cabecalho:
        return df[consulta].values
    else:
        for i, text in df.iterrows():
            for key, value in text[i].items():
                if consulta in key:
                    # Usa expressão regular para extrair o texto dentro das chaves
                    match = re.search(r'{([^}]*)}', text[i][consulta])
                    if match:
                        informacoes.append(match.group(1))
                else:
                    pass
        
        return informacoes

# Exemplo de uso:
arquivo_csv = 'csv-files\\abev3.csv'  # Substitua pelo caminho do seu arquivo CSV
consulta = 'Nome de Pregão'  # Consulta desejada

resultado = extrair_informacao(arquivo_csv, consulta)
print(resultado)