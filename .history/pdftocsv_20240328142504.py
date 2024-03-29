import pypdfium2 as pdfium
import pandas as pd
import csv
import os

def organyze_text(text_all):
    sentences = []
    words = ''
    for char in text_all:
      if char == '\n' or char == '\r':
        if words:
          sentences.append(words)
          words = ''
      else:
        words += char
    return sentences

def create_tables(sentences_page:dict):
  df = pd.DataFrame(sentences_page.items(), columns=['filename', 'content'])
  return df

def scrapping(url):
  sentences_pages = {}
  for root, dirs, files in os.walk(url):
      for file in files:
          all_pages = []
          filepath = os.path.join(root, file)
          if file.endswith(".pdf"):
            pdf = pdfium.PdfDocument(filepath)
            num_pages = len(pdf)
            for i in range(num_pages):
              page = pdf[i]
              textpage = page.get_textpage()
              text_all = textpage.get_text_range()
              sentences_page = organyze_text(text_all)
              all_pages.append(sentences_page)
            sentences_pages[file] = sum(all_pages, [])

  list_dataframe = create_tables(sentences_pages)

  return list_dataframe

def tratamento(sentences):
  i = len(sentences) - 1
  temp = ''
  concatenate = set()
  added_once = False
  temp_processed = False

  while i >= 0:
    if '/' in sentences[i-1] and sentences[i-1].endswith('a'):
      sentences[i-1] = f'{sentences[i-1]} {sentences[i]}'
      del sentences[i]

    elif sentences[i][-1] == ':' or ':' in sentences[i]:
      if temp:
          concatenate.add(temp)
          temp=''
          temp_processed = False
      temp+=sentences[i]

    if not temp_processed and temp:
      temp_split = temp.split(":")
      if len(temp_split) > 1 and temp_split[1]:
        if "//" in temp_split[1] and "www" in temp_split[1]:
          print(f"atual valor de senteces é:{sentences[i]}, índice anterior é {i-1} e tem isso: {sentences[i-1]}. O índice posterior é {i} e tem isso: {sentences[i+1]}")
          #print(f"O temp foi dividido em: primeira parte - {temp_split[0]} e segunda parte - {temp_split[1]}")
          if temp.find(' ') != -1:
            sentences[i] = temp.split(" ")[0]
        else:
          concatenate.add(temp_split[1]+':')
          sentences[i] = temp_split[0]+':'
          sentences.insert(i + 1, temp_split[1].strip())
        #print(f"posição original {sentences[i]}, um índice a frente {sentences[i+1]}, dois índices a frente {sentences[i+2]}")
      else:
        if not added_once:
          concatenate.add(temp)
          added_once = True
      temp_processed=True
    i -= 1

    if 'Balanço Patrimonial - Consolidado' in sentences[i]:
        word = sentences[i].split(" ")
        words = [' '.join(word[:-2]), word[-2], word[-1]]
        sentences[i] = ' '.join(word[:-2])
        sentences.insert(i+1,word[-2])
        sentences.insert(i+2,word[-1])

    if 'Composição do Capital Social' in sentences[i]:
        sentences[i] = sentences[i] + ' ' +sentences[i+1]
        del sentences[i+1]

    if 'Ações em Circulação no Mercado' in sentences[i]:
        sentences[i] = sentences[i] + ' - ' + sentences[i+1]
        words = sentences[i+2].split(" ")
        del sentences[i+1]
        sentences.insert(i + 1, ' '.join(words[:-2]))
        sentences.insert(i + 2, words[-2])
        sentences.insert(i + 3, words[-1])
        del sentences[i+4]

    if 'Posição Acionária*' in sentences[i]:
        words = sentences[i+1].split(" ")
        del sentences[i+1]
        sentences.insert(i + 1, words[-4])
        sentences.insert(i + 2, words[-3])
        sentences.insert(i + 3, words[-2])
        sentences.insert(i + 4, words[-1])

  return sentences

def tratamento_geral(data):
  dicionarios = {}
  dicionario1 = {}
  contact_passed = False
  contact_value = ''
  palavras_chave = ["Balanço Patrimonial - Consolidado",
                    "Demonstração do Resultado - Consolidado",
                    "Demonstração do Fluxo de Caixa - Consolidado",
                    "Posição Acionária",
                    "Ações em Circulação no Mercado",
                    "Composição do Capital Social"]

  # Realizando os pré-processamentos dos dados
  lista = tratamento(data)
  #print(lista)
  # Etapa de tratamento geral do PDF
  for i in range(len(lista)):
      if lista[i].endswith(":"):
          chave = lista[i][:-1]  
          valor = ""  # Inicializando o valor como uma string vazia
          j = i + 1  # Índice para iterar sobre os elementos após a coluna
          # Concatenando os elementos subsequentes até encontrar outro elemento terminado em ":", pois seria a outra coluna
          while j < len(lista) and not lista[j].endswith(":") and not ":" in lista[j]:
              valor += lista[j] + " "
              j += 1
          valor = valor.strip()  # Removendo espaços em branco extras do valor
          dicionario1[chave] = valor  # Adicionando a chave e o valor ao dicionário
      elif ":" in lista[i] and not lista[i].endswith(":"): 
          word = lista[i].split(":")
          chave = word[0]+":"
          valor = word[0]
      elif contact_passed:
        if "Dados Econômico-Financeiros" in lista[i] or "Balanço Patrimonial - Consolidado" in lista[i]:
            contact_passed = False
        else:
            contact_value += lista[i] + " "
      elif "Plantão de Notícias" in lista[i]:
          contact_passed = True

      #others pages
      for palavra_chave in palavras_chave:
        if palavra_chave in lista[i]:
          # Inicializando o dicionário para esta palavra-chave
          if palavra_chave in "Posição Acionária*":
            #Formato: 'Nome %ON %PN %Total'
            dicionario = {}
            dicionarios[lista[i]] = dicionario
            colunas = [lista[i+1], lista[i+2], lista[i+3], lista[i+4]]
            break

          if palavra_chave in "Composição do Capital Social": 
            dicionario = {}
            dicionarios[lista[i]] = dicionario
            colunas = ['Nomes', 'Valores']
            break

          if palavra_chave in "Ações em Circulação no Mercado": 
            dicionario = {}
            dicionarios[lista[i]] = dicionario
            colunas = [lista[i+1], lista[i+2], lista[i+3]]
            break

          dicionario = {}
          dicionarios[lista[i]] = dicionario
          colunas = [lista[i], lista[i+1], lista[i+2]]
          break

      # Se encontramos uma palavra-chave, processamos os elementos seguintes até a próxima palavra-chave ou o final da lista
      if lista[i] in dicionarios:
          index_elemento = lista.index(lista[i])
          linhas = []
          if "Composição do Capital Social" in lista[i]:
            for j in range(index_elemento+1, len(lista)):
              if any(palavra_chave in lista[j] for palavra_chave in palavras_chave):
                  break
              else:
                  words = lista[j].split(" ")
                  if len(words) > 1 and "/" not in lista[j]:
                    words = lista[j].split(" ")
                    linhas.append([words[0], words[1]])
                  else:
                    linhas.append([words[0], ''])

          if "Posição Acionária*" in lista[i]:
            for j in range(index_elemento + 5, len(lista)):
              if any(palavra_chave in lista[j] for palavra_chave in palavras_chave):
                  break
              else:
                  words = lista[j].split(" ")
                  if "Total" in words:
                    linhas.append([' '.join(words[:-3]),words[-3], words[-2], words[-1]])
                    break
                  elif not any(map(str.isdigit, lista[j+1])) and not "%" in lista[j+1]:
                    concatenate_words = lista[j+1] + ' ' + lista[j+2]
                    words = lista[j+3].split(" ")
                    lista[j+1] = concatenate_words + lista[j+3]
                    linhas.append([' '.join(words[:-3]),words[-3], words[-2], words[-1]])
                  else:
                    linhas.append([' '.join(words[:-3]),words[-3], words[-2], words[-1]])

          else:
            for j in range(index_elemento + 3, len(lista)):
                if any(palavra_chave in lista[j] for palavra_chave in palavras_chave):
                    break
                else:
                    words = lista[j].split(" ")
                    if len(words) > 1:
                      linhas.append([' '.join(words[:-2]), words[-2], words[-1]])

          # Preenchendo o dicionário
          for j, coluna in enumerate(colunas):
              dicionarios[lista[i]][coluna] = [linha[j] for linha in linhas]

  dicionario1["Plantão de Notícias delay de 15 min."] = contact_value.strip()
  dicionarios['Dados da Companhia'] = dicionario1

  # Mesclando dicionários
  resultado = { 'Dados da Companhia': dicionario1, **dicionarios}

  return resultado

def flatten_dict(d):
    flattened_dict = {}
    for sub_dict in d.values():
        for key, value in sub_dict.items():
            flattened_dict[key] = value

    return flattened_dict

def convert_csv(data, filename):
    with open(filename, 'w', newline='', encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        # Escrever cabeçalhos (chaves do dicionário) como a primeira linha
        writer.writerow(data.keys())
        # Escrever valores (linhas do dicionário) como linhas subsequentes
        writer.writerow(data.values())

def pdftocsv(csv_path):
  dados = scrapping('pdfs')
  if not os.path.exists(csv_path):
    os.makedirs(csv_path)

  for index, row in dados.iterrows():
      file = row['filename']
      content = row['content']
      filename = file.split(".")[0]
      filepath = f'{csv_path}/{filename}.csv'
      pdf = tratamento_geral(content)
      pdf_flatted = flatten_dict(pdf)
      convert_csv(pdf_flatted, filepath)

pdftocsv('csv_files')