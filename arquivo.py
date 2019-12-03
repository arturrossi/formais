def extrai_listas_linha1(string, lista_original):
    linha1 = string[0]
    quant = 0
    for indice in range(0, len(linha1)): #passa sobre os caracteres da primeira linha ate achar '{', onde começam as informações do automato
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
        i = 1
        tamanho = len(linha[indice])
        while linha[indice][i] != ")":
            i += 1
        lista = list(linha[indice][1:i].split(","))  # pega as informações de dentro da transição sem os parentesis e a virgula. (q0,a) fica 'q0', 'a'
        j = i + 2 #se o i para um caractere antes do ")", e após isso há um "=", como por exemplo "(q0,a)=q1", entao deve-se pular 2 caracteres para chegar no estado de destino
        estado_destino_transicao = linha[indice][j:tamanho]
        lista.append(estado_destino_transicao)
        lista_final.append(lista)
    return lista_final


def extrai_palavras(reader):
    lista_palavras = []
    for coluna in reader:
        lista_palavras.append(coluna)
    return lista_palavras