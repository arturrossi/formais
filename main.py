import arquivo
import automatos

with open('teste2.txt', 'rt') as file:
    linhas = file.readlines()


estados = []
infos = arquivo.extrai_listas_linha1(linhas, estados)

transicoes = arquivo.extrai_listas_transicoes(linhas)

#print(infos)
#print(transicoes)

afn = automatos.AFN()
afn.define_afn(infos, transicoes)

afd = automatos.AFD()
afd.converter_afn_para_afd(afn)
afd.minimizar_afd()
