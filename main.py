import arquivo
import automatos
import csv

with open('teste8.txt', 'rt') as file:
    linhas = file.readlines()

with open('palavras2.txt') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    palavras = arquivo.extrai_palavras(csv_reader)

estados = []
infos = arquivo.extrai_listas_linha1(linhas, estados)

transicoes = arquivo.extrai_listas_transicoes(linhas)

afn = automatos.AFN()
afn.define_afn(infos, transicoes)

afd = automatos.AFD()
afd.converter_afn_para_afd(afn)
afd.minimizar_afd()
afd.avalia_palavras(palavras)

with open('afd_gramatica.txt') as file2:
    linhas2 = file2.readlines()

estados = []
infos = arquivo.extrai_listas_linha1(linhas2, estados)

transicoes = arquivo.extrai_listas_transicoes(linhas2)

afd_2 = automatos.AFD()
afd_2.define_afd(infos, transicoes)
afd_2.afd_pra_gramatica()
