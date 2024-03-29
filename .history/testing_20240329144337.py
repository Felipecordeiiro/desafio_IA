asks_tables = [
    'Dados da Companhia',
    'Balanço Patrimonial - Consolidado',
    'Demonstração do Resultado - Consolidado',
    'Demonstração do Fluxo de Caixa - Consolidado',
    'Posição Acionária*',
    'Ações em Circulação no Mercado',
    'Composição do Capital Social'
]

# Cria a string formatada
informacoes_gerais = "Informações gerais sobre um arquivo, como:\n{}".format("\n".join("\t{}".format(item) for item in asks_tables))

# Imprime a string formatada
print(informacoes_gerais)