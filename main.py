import arquivo
import automatos
import csv

with open('teste2.txt', 'rt') as file:
    linhas = file.readlines()

with open('palavras.txt') as csv_file:
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
