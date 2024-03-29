import os
import ast
import pandas as pd

def extrair_informacao(filename_csv, consulta):
    csv_folder = 'csv-files'
    csv_files = os.listdir(csv_folder)

    # Tratamento do nome do arquivo
    if filename_csv.endswith(".csv"):
        pass
    else:
        filename_csv = filename_csv + '.csv'

    if filename_csv in csv_files:
        csv_files = [os.path.join(csv_folder, file) for file in csv_files if file.endswith(".csv")]
        for filepath in csv_files:
            if filename_csv == csv_file:
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

consulta = 'Dados da Companhia'  # Consulta desejada
arquivo = 'bbse3'

resultado = extrair_informacao(arquivo, consulta)
print(resultado)