import os
import ast
import pandas as pd

def extrair_informacao(filename_csv, consulta):
    csv_folder = 'csv-files'
    csv_files = os.listdir(csv_folder)
    [cs]
    if filename_csv in 
    for csv_file in csv_files:
        df = pd.read_csv(csv_file, encoding='utf-8')
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
  # Substitua pelo caminho do seu arquivo CSV
consulta = 'Dados da Companhia'  # Consulta desejada

resultado = extrair_informacao(csv_folder, consulta)
print(resultado)