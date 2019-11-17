def extrai_listas_linha1(string, lista_original):
    linha1 = string[0]
    quant = 0
    for indice in range(0, len(linha1)):
        if linha1[indice] == '{':
            comeco = indice + 1
            quant += 1
            while linha1[indice] != '}':
                indice = indice + 1
            lista_original.append(list(linha1[comeco:indice].split(",")))
            if quant == 2:
                estado_inicial = list(linha1[indice + 2:indice + 4].split(" "))
                lista_original.append(estado_inicial)
    return lista_original


def extrai_listas_transicoes(linha):
    lista_final = []
    for indice in range(2, len(linha)):
        lista = list(linha[indice][1:5].split(","))
        estado_destino_transicao = linha[indice][7:9]
        lista.append(estado_destino_transicao)
        lista_final.append(lista)
    return lista_final


def extrai_palavras(reader):
    lista_palavras = []
    for coluna in reader:
        lista_palavras.append(coluna)
    return lista_palavras