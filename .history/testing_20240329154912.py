asks = {
        'datetime_atualizacao': 'Quando o relatório do {} foi atualizado?',
        'cod_negociacao': 'Qual o códigos de negociação do {}?',
        'cnpj': 'Qual o CNPJ do {}?',
        'atv_principal': 'Qual a atividade principal do {}?',
        'class_setorial': 'Qual a classificação setorial do {}?',
        'site': 'Qual o site do {}?',
        'contato': 'Quais os contatos do {}?',
        'plantao_noticias': 'Quais as noticias do {}?',
        'balanco_patrimonial': 'Qual o periodo do Balanço Patrimonial do {}?',
        'ativo_imobilizado': 'Qual é o ativo imobilizado do {}?',
        'ativo_total': 'Qual é o ativo total do {}?',
        'patrimonio_liquido': 'Qual é o pratimônio liquido do {}?',
        'patrimonio_liquido_controladora': 'Qual é o Patrimônio Líquido Atribuído à Controladora do {}?',
        'demonstracao_resultado': 'Quais os períodos da demonstração de resultados do {}?',
        'receita_de_venda': 'Qual é a Receita de Venda do {}?',
        'resultado_bruto': 'Qual é a Resultado Bruto do {}?',
        'resultado_de_equivalencia': 'Qual é o Resultado de Equivalência Patrimonial do {}?',
        'resultado_financeiro': 'Qual é a Resultado Financeiro do {}?',
        'resultado_liquido_continuado': 'Qual é a Resultado Líquido das Operações Continuadas do {}?',
        'lucro_prejuizo': 'Qual é o Lucro Prejuízo do Período do {}?',
        'lucro_prejuizo_controladora': 'Qual é o Lucro Prejuízo do Período Atribuído à Controladora do {}?',
        'demonstracao_fluxo_de_caixa': 'Qual é o período da Demonstração do Fluxo de Caixa do {}?',
        'atividades_operacionais': 'Quais é o valor das Atividades Operacionais do {}?',
        'atividades_de_investimento': 'Quais é o valor das Atividades de Investimento do {}?',
        'atividade_de_financiamento': 'Quais é o valor das Atividades de Financiamento do {}?',
        'avariacao_cambial': 'Quais é o valor das Variação Cambial sobre Caixa e Equivalentes do {}?',
        'aumento_reducao': 'Quais é o valor do Aumento (Redução) de Caixa e Equivalentes do {}?',
        'posicao_acionaria': 'Quais as Posições Acionárias do {}?',
        'informacoes_posicao_acionaria_recebida_em': 'Quando as posições acionárias do {} foram recebidas?',
        'acoes_em_circulacao_mercado': 'Quais as Ações em Circulação no Mercado do {}?',
        'composicao_capital_social': 'Qual a Composição do Capital Social do {}?'
}

for ask in asks:
    print(asks[ask])
                            csv_line[ask],