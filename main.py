import arquivo
import automatos
import csv

#####################################################################

#recebe um AFN M e cria seu AFD M minimizado

with open('automatos_entrada/teste_trab.txt', 'rt') as file:
    linhas = file.read().splitlines()#lê as linhas do arquivo de entrada do AFN

estados = []
infos = arquivo.extrai_listas_linha1(linhas, estados) #extrai as informações da primeira linha do arquivo, ou seja, estado inicial, estados finais, alfabeto, etc

transicoes = arquivo.extrai_listas_transicoes(linhas) #extrai as informações das transições do autômato

afn = automatos.AFN() #cria um AFN vazio
afn.define_afn(infos, transicoes) #põe as informações do automato dentro de listas, tuplas e dicionários

afd = automatos.AFD() #cria um AFD vazio
afd.converter_afn_para_afd(afn) #converte o AFN para AFD
afd.minimizar_afd() #minimiza o AFD

#####################################################################

#recebe um arquivo csv e decide quais palavras o AFD M minimizado aceita e quais ele rejeita

with open('palavras/palavras_trab.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',') #abre o arquivo CSV com as palavras de entrada
    palavras = arquivo.extrai_palavras(csv_reader) #le as colunas do arquivo (cada coluna tem uma palavra)
afd.avalia_palavras(palavras) #avalia as palavras a partir do automato minimizado

#####################################################################

#recebe um AFD e cria um uma Gramatica Regular

with open('automatos_entrada/teste9.txt') as file2:
    linhas2 = file2.read().splitlines() #le o arquivo de entrada com as informações do AFD

estados = []
infos = arquivo.extrai_listas_linha1(linhas2, estados) #extrai as informações da primeira linha do arquivo, ou seja, estado inicial, estados finais, alfabeto, etc

transicoes = arquivo.extrai_listas_transicoes(linhas2) #extrai as informações das transições do autômato

afd_2 = automatos.AFD() #cria um AFD vazio
afd_2.define_afd(infos, transicoes) #põe as informações do automato dentro de listas, tuplas e dicionários
afd_2.afd_pra_gramatica() #cria uma Gramática Regular a partir do autômato

#####################################################################

#recebe dois automatos e decide se ACEITA(M1) = ACEITA(M2)

with open('automatos_entrada/teste10.txt') as file3:
    linhas3 = file3.read().splitlines() #le o arquivo de entrada com as informações do AFD

estados = []
infos = arquivo.extrai_listas_linha1(linhas3, estados) #extrai as informações da primeira linha do arquivo, ou seja, estado inicial, estados finais, alfabeto, etc

transicoes = arquivo.extrai_listas_transicoes(linhas3) #extrai as informações das transições do autômato

afd_3 = automatos.AFD() #cria um AFD vazio
afd_3.define_afd(infos, transicoes) #põe as informações do automato dentro de listas, tuplas e dicionários
complementar_3 = afd_3.automato_complementar() #cria o automato complementar de M1


with open('automatos_entrada/teste11.txt') as file4:
    linhas4 = file4.read().splitlines() #le o arquivo de entrada com as informações do AFD

estados = []
infos = arquivo.extrai_listas_linha1(linhas4, estados) #extrai as informações da primeira linha do arquivo, ou seja, estado inicial, estados finais, alfabeto, etc

transicoes = arquivo.extrai_listas_transicoes(linhas4) #extrai as informações das transições do autômato

afd_4 = automatos.AFD() #cria um AFD vazio
afd_4.define_afd(infos, transicoes) #põe as informações do automato dentro de listas, tuplas e dicionários
complementar_4 = afd_4.automato_complementar() #cria o automato complementar de M2

if afd_3.alfabeto != afd_4.alfabeto: #apenas compara automatos que tem o mesmo alfabeto. Se nao tiverem o mesmo alfabeto, manda uma mensagem para o usuario
    print('Por favor, entre com automatos com alfabetos iguais!')
else:
    interseccao_1 = afd_3.interseccao_automatos(complementar_4) #faz a interseccao de M1 com o complemento de M2
    interseccao_2 = complementar_3.interseccao_automatos(afd_4) #faz a inteseccao do complemento de M1 com M2
    resultado = interseccao_1.uniao_automatos(interseccao_2) #faz a uniao de M1 com complemento de M2 e complemento de M1 com M2
    vazia = resultado.check_vazio() #se o resultado da união for uma linguagem vazia, entao M1 é igual a M2. Senão, são diferentes.
    if vazia:
        print('\n\nACEITA(M1) = ACEITA(M2)')
    else:
        print('\nACEITA(M1) \u2260 ACEITA(M2)')