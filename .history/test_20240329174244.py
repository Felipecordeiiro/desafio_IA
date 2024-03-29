import os 
import pandas as pd
import ast

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
                        dict_text = eval(text[0])
                        for i, lista in enumerate(dict_text.values(), len(dict_text.keys())):
                            if consulta in lista:
                                posição = lista.index(consulta)
                            else:
                                dicionario[consulta] = lista.index(posição]
                                return dicionario
                                    



#posicao = dados['Balanço Patrimonial - Consolidado'].index('Ativo Total')
# 'Dados da Companhia'
print(extrair_informacao('abev3', 'Ativo Total'))