import csv
import re

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

                        print(informacoes)
                        celula = linha[coluna]
                        if celula[consulta]:
                            # Usa expressão regular para extrair o texto dentro das chaves
                            match = re.search(r'{([^}]*)}', celula)
                            if match:
                                informacoes.append(match.group(1))
                        else:
                            print("Não foi possível encontrar essa informação")

        
        if indice_coluna is None:
            return "Não foi possível encontrar informações para essa consulta."
        '''
        for linha in reader:
            celula = linha[indice_coluna]
            # Usa expressão regular para extrair o texto dentro das chaves
            match = re.search(r'{([^}]*)}', celula)
            if match:
                informacoes.append(match.group(1))
        
        if not informacoes:
            return "Não foram encontradas informações para essa consulta."
        '''
        
        return informacoes

# Exemplo de uso:
arquivo_csv = 'csv-files\\abev3.csv'  # Substitua pelo caminho do seu arquivo CSV
consulta = "Nome de Pregão"  # Consulta desejada

resultado = extrair_informacao(arquivo_csv, consulta)
print(resultado)