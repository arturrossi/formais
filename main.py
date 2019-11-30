import arquivo
import automatos
import csv

with open('automatos_entrada/teste_trab.txt', 'rt') as file:
    linhas = file.readlines()

with open('palavras/palavras_trab.csv') as csv_file:
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

with open('automatos_entrada/teste9.txt') as file2:
    linhas2 = file2.readlines()

estados = []
infos = arquivo.extrai_listas_linha1(linhas2, estados)

transicoes = arquivo.extrai_listas_transicoes(linhas2)

afd_2 = automatos.AFD()
afd_2.define_afd(infos, transicoes)
afd_2.afd_pra_gramatica()

with open('automatos_entrada/teste10.txt') as file3:
    linhas3 = file3.readlines()

estados = []
infos = arquivo.extrai_listas_linha1(linhas3, estados)

transicoes = arquivo.extrai_listas_transicoes(linhas3)

afd_3 = automatos.AFD()
afd_3.define_afd(infos, transicoes)
complementar_3 = afd_3.automato_complementar()


with open('automatos_entrada/teste11.txt') as file4:
    linhas4 = file4.readlines()

estados = []
infos = arquivo.extrai_listas_linha1(linhas4, estados)

transicoes = arquivo.extrai_listas_transicoes(linhas4)

afd_4 = automatos.AFD()
afd_4.define_afd(infos, transicoes)
complementar_4 = afd_4.automato_complementar()

if afd_3.alfabeto != afd_4.alfabeto:
    print('Por favor, entre com automatos com alfabetos iguais!')
else:
    interseccao_1 = afd_3.interseccao_automatos(complementar_4)
    interseccao_2 = complementar_3.interseccao_automatos(afd_4)
    resultado = interseccao_1.uniao_automatos(interseccao_2)
    vazia = resultado.check_vazio()
    if vazia:
        print('\n\nACEITA(M1) = ACEITA(M2)')
    else:
        print('\nACEITA(M1) \u2260 ACEITA(M2)')