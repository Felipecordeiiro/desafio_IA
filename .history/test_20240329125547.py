import csv
import re
import ast
import pandas as pd

def extrair_informacao(arquivo_csv, consulta):
    csv_files = os.list
    df = pd.read_csv(arquivo_csv, encoding='utf-8')
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

# Exemplo de uso:
csv_folder = 'csv-files'  # Substitua pelo caminho do seu arquivo CSV
consulta = 'Dados da Companhia'  # Consulta desejada

resultado = extrair_informacao(csv_folder, consulta)
print(resultado)