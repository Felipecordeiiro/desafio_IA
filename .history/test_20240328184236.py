import os
import csv

def extrair_informacao(arquivo_csv, empresa, consulta):
    with open(arquivo_csv, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        cabecalho = next(reader)  # Lê o cabeçalho

        if consulta.lower().startswith("sobre"):
            # Remova a palavra "sobre" da consulta
            consulta = consulta[6:].strip()

        if consulta.lower() == "site":
            # Verifica se a consulta é para acessar o site
            for linha in reader:
                for celula in linha:
                    if empresa.lower() in celula.lower():
                        match = re.search(r'{([^}]*)}', celula)
                        if match:
                            informacoes = match.group(1)
                            return informacoes
            return "Não foi possível encontrar o site da empresa {}.".format(empresa)
        else:
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
                if linha[0].lower() == empresa.lower():
                    celula = linha[indice_coluna]
                    # Usa expressão regular para extrair o texto dentro das chaves
                    match = re.search(r'{([^}]*)}', celula)
                    if match:
                        informacoes.append(match.group(1))

            if not informacoes:
                return "Não foram encontradas informações para essa consulta."

            return informacoes

# Supondo que 'csv_dir' seja o diretório onde estão seus arquivos CSV
arquivo_csv = os.path.join('csv-files', 'nome_do_arquivo.csv')
empresa = "AMBEV"
consulta = "Balanço Patrimonial"

informacao = extrair_informacao(arquivo_csv, empresa, consulta)
print(informacao)
