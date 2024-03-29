import csv
import re
import ast

def extrair_informacao(arquivo_csv, consulta):
    with open(arquivo_csv, encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        cabecalho = next(reader)  # Lê o cabeçalho
        informacoes = []
        # Encontra o índice da coluna correspondente à consulta
        indice_coluna = None
        for i, coluna in enumerate(cabecalho):
            if consulta.lower() in coluna.lower():
                indice_coluna = i
                break
            else:
                for text in reader:
                    for information in text:
                        dict_info = ast.literal_eval(information)
                        if dict_info[consulta]:
                            print(dict_info[continue])
                            # Usa expressão regular para extrair o texto dentro das chaves
                            match = re.search(r'{([^}]*)}', dict_info[consulta])
                            if match:
                                informacoes.append(match.group(1))
                                break
                        else:
                            pass

        
        if indice_coluna is None:
            return "Não foi possível encontrar informações para essa consulta."
        
        return informacoes

# Exemplo de uso:
arquivo_csv = 'csv-files\\abev3.csv'  # Substitua pelo caminho do seu arquivo CSV
consulta = 'Nome de Pregão'  # Consulta desejada

resultado = extrair_informacao(arquivo_csv, consulta)
print(resultado)