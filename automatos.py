import collections
import itertools
import copy
import string

class AFN:
    def __init__(self):
        self.inicial = ''
        self.finais = []
        self.transicoes = []
        self.alfabeto = []
        self.estados = []
        self.dicionario_transicoes_afn = {}

    def define_afn(self, lista, transicoes):
        self.estados = lista[0]
        self.alfabeto = lista[1]
        self.inicial = lista[2]
        self.finais = lista[3]

        for elemento in transicoes:
            estado_inicial = elemento[0]
            letra_transicao = elemento[1]
            estado_destino = elemento[2]
            funcao_transicao = (estado_inicial, letra_transicao, estado_destino)
            self.transicoes.append(funcao_transicao)

        for elemento in self.transicoes:
            if (elemento[0], elemento[1]) in self.dicionario_transicoes_afn:
                self.dicionario_transicoes_afn[(elemento[0], elemento[1])].append(elemento[2])
            else:
                self.dicionario_transicoes_afn[(elemento[0], elemento[1])] = [elemento[2]]

#retorna o a lista de estados ordenada, por exemplo [['q3'], ['q2'], ['q1']] retorna [['q1'], ['q2'], ['q3']]
def retorna_maior(lista_estados):
    lista_estados.sort()
    return lista_estados

#concatena os estados maiores que 1 em uma lista em apenas um só, como, por exemplo [q2, q3] em [q2q3]
def concatena_estados_lista(lista):
    for item in lista:
        if len(item) > 1:
            retorna_maior(item)
            junta_estados = ''.join(item)
            lista.remove(item)
            lista.append([junta_estados])



#transforma estados de tamanho maior que 1 em apenas um só, concatenando-os, por exemplo [['q2'], ['q3']] em ['q2q3']
def concatena_estados_transicoes(dicionario):
    auxiliar = {}
    for item,value in dicionario.items():
        if len(value) > 1:
            retorna_maior(value)
            junta_estados = ''.join(value)
            dicionario[item] = [junta_estados]
        if len(item[0][0]) > 1:
            item_aux = list(item[0])
            retorna_maior(item_aux)
            junta_estados = ''.join(item_aux)
            auxiliar[item] = (junta_estados, item[1])

    for velho, novo in auxiliar.items():
        dicionario[novo] = dicionario.pop(velho)

class AFD:
    def __init__(self):
        self.inicial = ''
        self.finais = []
        self.dicionario_transicoes_afd = {}
        self.alfabeto = []
        self.estados_visitados = []
        self.transicoes = []

    def define_afd(self, lista, transicoes):
        self.estados_visitados = lista[0]
        self.alfabeto = lista[1]
        self.inicial = lista[2]
        self.finais = lista[3]

        for elemento in transicoes:
            estado_inicial = elemento[0]
            letra_transicao = elemento[1]
            estado_destino = elemento[2]
            funcao_transicao = (estado_inicial, letra_transicao, estado_destino)
            self.transicoes.append(funcao_transicao)

        for elemento in self.transicoes:
            self.dicionario_transicoes_afd[(elemento[0], elemento[1])] = [elemento[2]]


    def converter_afn_para_afd(self, afn):
        self.alfabeto = afn.alfabeto
        self.inicial = afn.inicial

        #adiciona inicial aos estados visitados
        self.estados_visitados.append(self.inicial)

        for estado in self.estados_visitados:
            numero_estados = len(estado)
            if numero_estados == 1:
                for simbolo in self.alfabeto:
                    if (estado[0], simbolo) in afn.dicionario_transicoes_afn:
                        self.dicionario_transicoes_afd[(estado[0], simbolo)] = afn.dicionario_transicoes_afn[(estado[0],simbolo)]
                        if afn.dicionario_transicoes_afn[(estado[0],simbolo)] not in self.estados_visitados:
                            self.estados_visitados.append(afn.dicionario_transicoes_afn[(estado[0], simbolo)])
            else:
                for simbolo in self.alfabeto:
                    lista_aux = []
                    lista_final = []
                    for estados in estado:
                        if (estados, simbolo) in afn.dicionario_transicoes_afn:
                            novo = afn.dicionario_transicoes_afn[(estados, simbolo)]
                            lista_aux.extend(novo)
                    if lista_aux:
                        lista_final.extend(list(set(lista_aux).union(lista_aux)))
                        self.dicionario_transicoes_afd[(tuple(estado), simbolo)] = lista_final
                        if novo not in self.estados_visitados:
                            self.estados_visitados.append(lista_final)

        for estados in afn.finais:
            for estado in self.estados_visitados:
                if estados in estado:
                    self.finais.append(estado)


    #cria um estado que completa a transição daqueles estados que não tem uma transicao para um terminal do alfabeto
    def funcao_total(self):
        estado_aux = 'qaux'
        self.estados_visitados.append([estado_aux])
        for simbolos in self.alfabeto:
            self.dicionario_transicoes_afd[(estado_aux, simbolos)] = [estado_aux]
        lista_aux = []

        for estados in self.estados_visitados:
            for simbolo in self.alfabeto:
                if (estados[0], simbolo) not in self.dicionario_transicoes_afd:
                    lista_aux.append([(estados[0], simbolo, estado_aux)])

        for itens in lista_aux:
            self.dicionario_transicoes_afd[(itens[0][0], itens [0][1])] = [itens[0][2]]


    def remove_estados_inalcancaveis(self):
        g = collections.defaultdict(list)

        #junta todos os estados alcancaveis pelo defaultdict
        for key,value in self.dicionario_transicoes_afd.items():
            g[key[0]].append(value)

        #faz depth first search
        stack = copy.deepcopy(self.inicial)
        estados_alcancaveis = set()

        while stack:
            estado = stack.pop()
            if type(estado) is str:
                if estado not in estados_alcancaveis:
                        stack += g[estado]
                        estados_alcancaveis.add(estado)
            else:
                if estado[0] not in estados_alcancaveis:
                        stack += g[estado[0]]
                        estados_alcancaveis.add(estado[0])

        self.estados_visitados = [estado for estado in self.estados_visitados if estado[0] in estados_alcancaveis]

        self.finais = [estado for estado in self.finais if estado[0] in estados_alcancaveis]

        self.dicionario_transicoes_afd = {key:value for key,value in self.dicionario_transicoes_afd.items() if key[0] in estados_alcancaveis}

    def remove_estados_inuteis(self):
        estados_uteis = self.finais
        estados_uteis = list(itertools.chain(*estados_uteis))

        M = []
        flag = True

        while flag:
            flag = False
            for estado_final in estados_uteis:
                for estado in self.estados_visitados:
                    for simbolo in self.alfabeto:
                        transicao = self.dicionario_transicoes_afd.get((estado, simbolo))
                        if transicao is not None:
                            if transicao[0] == estado_final:
                                M.append(estado)
            antes = len(estados_uteis)
            estados_uteis = list(set(estados_uteis) | set(M))
            depois = len(estados_uteis)
            if depois > antes:
                flag = True


        estados_inuteis = []

        for estado in self.estados_visitados:
            if estado not in estados_uteis:
                estados_inuteis.append(estado)

        dicionario_transicoes_final = copy.deepcopy(self.dicionario_transicoes_afd)

        aux = {}
        for key,value in self.dicionario_transicoes_afd.items():
            for estado in estados_inuteis:
                if estado in key:
                    del dicionario_transicoes_final[key]
                else:
                    if estado in value:
                        del dicionario_transicoes_final[key]


        for estado in self.estados_visitados:
            if estado in estados_inuteis:
                self.estados_visitados.remove(estado)

        return dicionario_transicoes_final

    def minimizar_afd(self):
        concatena_estados_transicoes(self.dicionario_transicoes_afd)
        concatena_estados_lista(self.estados_visitados)
        concatena_estados_lista(self.finais)

        self.remove_estados_inalcancaveis()


        nao_total = 0

        for item in self.dicionario_transicoes_afd.items():
            for simbolo in self.alfabeto:
                if self.dicionario_transicoes_afd.get((item[0][0], simbolo)) is None:
                    nao_total = 1

        if nao_total:
            self.funcao_total()

        self.estados_visitados.sort()

        #inicializa a tabela, marcando aqueles itens em que ou o primeiro item é estado final ou o segundo
        tabela = {}
        for i,item in enumerate(self.estados_visitados):
            for item_2 in self.estados_visitados[i+1:]:
                tabela[(item[0], item_2[0])] = ((item in self.finais) and (item_2 not in self.finais)) or ((item not in self.finais) and (item_2 in self.finais))
        flag = True

        #completa a tabela procurando estados equivalentes
        while flag:
            flag = False
            for i, item in enumerate(self.estados_visitados):
                for item_2 in self.estados_visitados[i+1:]:
                    if tabela[(item[0], item_2[0])]:
                        continue
                    for simbolo in self.alfabeto:
                        transicao1 = self.dicionario_transicoes_afd.get((item[0], simbolo))
                        transicao2 = self.dicionario_transicoes_afd.get((item_2[0], simbolo))


                        #q2q3 deu false quando era o segundo parametro
                        if transicao1 is not None and transicao2 is not None and transicao1 != transicao2:
                            marca = tabela.get((transicao1[0], transicao2[0]))
                            if marca is None:
                                marca = tabela.get((transicao2[0], transicao1[0]))

                            flag = flag or marca
                            tabela[(item[0], item_2[0])] = marca

                            if marca:
                                break


        novos_estados = []
        #cria uma lista com os novos estados, ou seja, aqueles estados que resultaram em falso (que nao foram marcados na tabela)
        for item,value in tabela.items():
            if not value:
                novos_estados.append(item)

        #transforma lista de tuplas pra lista de listas
        novos_estados = list(map(list, novos_estados))


        #junta os novos estados que englobam mais de um estado, por ex: [q2,q3], [q2,q4], [q3,q4] junta em [q2,q3,q4]
        if len(novos_estados) > 1:
            for i,dupla in enumerate(novos_estados):
                for elemento in dupla:
                    for proximos in novos_estados[i+1:]:
                        if elemento in proximos:
                            if elemento is proximos[0]:
                                if proximos[1] not in dupla:
                                    dupla.append(proximos[1])
                                    novos_estados.remove(proximos)
                                else:
                                    novos_estados.remove(proximos)
                            else:
                                if proximos[0] not in dupla:
                                    dupla.append(proximos[0])
                                    novos_estados.remove(proximos)
                                else:
                                    novos_estados.remove(proximos)

        novos_estados_finais = []
        # se algum dos estados antes da junçao era final, entao o novo estado é final também
        for estados in novos_estados:
            for estado in estados:
                for finais in self.finais:
                    for final in finais:
                        if estado is final:
                            novos_estados_finais.append(estado)
                            self.finais.remove(finais)

        novo_estado_inicial = []
        #se algum dos estados antes da juncao era inicial, entao o novo estado é inicial também
        for estados in novos_estados:
            for estado in estados:
                if estado == self.inicial[0]:
                    estado = ''.join(estados)
                    self.inicial = estado

        if not novos_estados_finais:
            novos_estados_finais = self.finais
            concatena_estados_lista(novos_estados_finais)
        else:
            novos_estados_finais = [''.join(novos_estados_finais)]
            self.finais.append(novos_estados_finais)
            self.finais.sort()


        #deleta as transicoes dos estados iguais comecando do segundo em frente, por ex:
        #se [q2,q3,q4] sao apenas um estado, deixa apenas as transicoes do q2 e deleta as do q3 e q4
        for estados in novos_estados:
            i = len(estados)
            for estado in estados[1:i]:
                for simbolo in self.alfabeto:
                    del self.dicionario_transicoes_afd[(estado, simbolo)]

        #troca todas as ocorrencias dos novos estados nas origens das transicoes, por ex:
        #se um novo estado é [q0,q1] (os novos estados ja estarao ordenados em ordem crescente)
        #troca as ocorrencias de q0 para q0,q1 e nao troca as de q1 pois ja foram deletadas anteriormente
        auxiliar = {}
        for estados in novos_estados:
            estado = estados[0]
            estados = tuple(estados)
            for keys in self.dicionario_transicoes_afd.keys():
                if keys[0] is estado:
                    self.dicionario_transicoes_afd[(estados, keys[1])] = self.dicionario_transicoes_afd[keys]
                    del self.dicionario_transicoes_afd[keys]

        #troca todas as ocorrencias dos novos estados nos resultados das transicoes, por ex:
        #se um novo estado é [q0,q1] e existe uma transicao (q2,a) = [q0] ou [q1], troca a transicao para (q2,a) = [q0,q1]
        for key,value in self.dicionario_transicoes_afd.items():
            for estados in novos_estados:
                if value[0] in estados:
                    self.dicionario_transicoes_afd[key] = estados

        concatena_estados_transicoes(self.dicionario_transicoes_afd)

        todos_estados = []

        for key in self.dicionario_transicoes_afd.keys():
            if key[0] not in todos_estados:
                todos_estados.append(key[0])

        self.estados_visitados = todos_estados
        dicionario_transicoes_final = self.remove_estados_inuteis()

        dicionario_transicoes_final = collections.OrderedDict(sorted(dicionario_transicoes_final.items()))
        self.dicionario_transicoes_afd = dicionario_transicoes_final


        print('AUTOMATO MINIMO')
        print("TRANSICOES:", self.dicionario_transicoes_afd)
        print('ESTADOS FINAIS:', self.finais)
        print("ESTADO INICIAL:", self.inicial)

    def avalia_palavras(self, palavras):
        teste_palavra = 'aaba'
        teste_palavra2 = 'bb'
        teste_palavra3 = 'ab'

        palavras_aceitas = []

        if not isinstance(self.inicial, list):
            transicao_i = [self.inicial]
        else:
            transicao_i = self.inicial

        for palavra in palavras:
            transicao = transicao_i
            if not palavra:
                if self.inicial in self.finais:
                    palavras_aceitas.append('palavra vazia')
            else:
                for char in palavra[0]:
                    destino = self.dicionario_transicoes_afd.get((transicao[0], char))
                    if destino is not None:
                        transicao = destino
                    else:
                        break
                if destino in self.finais:
                    palavras_aceitas.append(palavra[0])

        palavras = list(itertools.chain(*palavras))

        rejeitadas = set(palavras) - set(palavras_aceitas)
        rejeitadas = list(rejeitadas)
        print("ACEITA:", palavras_aceitas)
        print("REJEITA:", rejeitadas)

    def afd_pra_gramatica(self):
        inicial = False
        tabela_hash_estados_variaveis = {}
        #cria uma tabela hash referenciado o estado à sua respectiva variavel
        if self.estados_visitados[0] == self.inicial[0]:
            tabela_hash_estados_variaveis[self.estados_visitados[0]] = 'S'
            tamanho = len(self.estados_visitados)
            i = 1
            while i != tamanho:
                tabela_hash_estados_variaveis[self.estados_visitados[i]] = string.ascii_letters[i-1].capitalize()
                i += 1
        else:
            for i,estados in enumerate(self.estados_visitados):
                j = i - 1
                if estados == self.inicial[0]:
                    tabela_hash_estados_variaveis[self.estados_visitados[i]] = 'S'
                    inicial = True
                else:
                    if inicial:
                        tabela_hash_estados_variaveis[self.estados_visitados[i]] = string.ascii_letters[j].capitalize()
                    else:
                        tabela_hash_estados_variaveis[self.estados_visitados[i]] = string.ascii_letters[i].capitalize()


        aux = []
        for values in tabela_hash_estados_variaveis.values():
            aux.extend(values)

        #escreve no arquivo a Gramatica Regular
        with open("saida_gramatica/saida_GR.txt", "w", encoding="utf-8") as f:
            print('G = ({' + ', '.join(aux) + '}' ',' , '{' + ', '.join(self.alfabeto) + '},', tabela_hash_estados_variaveis[self.inicial[0]] +',', 'P)', file=f)
            print('P', file=f)
            keyList = sorted(self.dicionario_transicoes_afd.keys())
            tamanho_lista = len(keyList)
            for key, value in self.dicionario_transicoes_afd.items():
                indice = keyList.index(key)
                if indice + 1 <= tamanho_lista - 1:
                    if keyList[indice+1][0] != key[0] and key[0] in self.finais:
                        print(tabela_hash_estados_variaveis[key[0]], ' -> ', key[1], tabela_hash_estados_variaveis[value[0]], file=f)
                        print(tabela_hash_estados_variaveis[key[0]], ' -> ' + '\u03b5', file=f)  #\u03b5 é o unicode para o epsilon (movimento vazio) para terminar a Gramatica
                    else:
                        print(tabela_hash_estados_variaveis[key[0]], ' -> ', key[1], tabela_hash_estados_variaveis[value[0]], file=f)
                else:
                    print(tabela_hash_estados_variaveis[key[0]], ' -> ', key[1], tabela_hash_estados_variaveis[value[0]], file=f)
                    if key[0] in self.finais:
                        print(tabela_hash_estados_variaveis[key[0]], ' -> ' + '\u03b5', file=f)

            for final in self.finais:
                if final not in self.dicionario_transicoes_afd:
                    print(tabela_hash_estados_variaveis[final], ' -> ' + '\u03b5', file=f)



    def automato_complementar(self):
        complementar = AFD()
        nao_total = 0
        for key in self.dicionario_transicoes_afd.keys():
            for simbolo in self.alfabeto:
                if self.dicionario_transicoes_afd.get((key[0], simbolo)) is None:
                    nao_total = 1
        if nao_total:
            self.estados_visitados = [[estado] for estado in self.estados_visitados]
            self.funcao_total()
            self.estados_visitados = list(itertools.chain.from_iterable(self.estados_visitados))

        complementar.dicionario_transicoes_afd = self.dicionario_transicoes_afd
        complementar.alfabeto = self.alfabeto
        complementar.estados_visitados = self.estados_visitados
        complementar.inicial = self.inicial

        for estado in self.estados_visitados:
            if estado not in self.finais:
                complementar.finais.append(estado)

        return complementar


    #faz interseccao de 2 automatos
    def interseccao_automatos(self, afd):
        novo_automato = AFD()

        novo_automato.alfabeto = self.alfabeto

        for estados in self.estados_visitados:
            for estados_2 in afd.estados_visitados:
                novo_automato.estados_visitados.append((estados,estados_2))

        novo_automato.inicial = (self.inicial[0], afd.inicial[0])

        for finais_1 in self.finais:
            for finais_2 in afd.finais:
                novo_automato.finais.append((finais_1, finais_2))


        for estados in novo_automato.estados_visitados:
            for simbolos in novo_automato.alfabeto:
                novo_automato.dicionario_transicoes_afd[(estados, simbolos)] =\
                    (self.dicionario_transicoes_afd.get((estados[0], simbolos)), afd.dicionario_transicoes_afd.get((estados[1], simbolos),))

        return novo_automato

    def uniao_automatos(self, afd):
        novo_automato = AFD()

        novo_automato.alfabeto = self.alfabeto

        for estados in self.estados_visitados:
            for estados_2 in afd.estados_visitados:
                novo_automato.estados_visitados.append((estados, estados_2))
                if estados in self.finais or estados_2 in afd.finais:
                    novo_automato.finais.append((estados, estados_2))

        novo_automato.inicial = (self.inicial, afd.inicial)

        for estados in novo_automato.estados_visitados:
            for simbolos in novo_automato.alfabeto:
                novo_automato.dicionario_transicoes_afd[(estados, simbolos)] = \
                    (self.dicionario_transicoes_afd.get((estados[0], simbolos)),
                     afd.dicionario_transicoes_afd.get((estados[1], simbolos)))

        for key,value in novo_automato.dicionario_transicoes_afd.items():
            novo_value = []
            for dupla in value:
                dupla = tuple(list(itertools.chain.from_iterable(dupla)))
                novo_value.append(dupla)
            novo_value = tuple(novo_value)
            novo_automato.dicionario_transicoes_afd[key] = novo_value

        return novo_automato

    def check_vazio(self):
        aux = [self.inicial]
        vazia = 1

        for item in aux:
         if vazia:
                for simbolo in self.alfabeto:
                    transicao = self.dicionario_transicoes_afd.get((item, simbolo))
                    if transicao not in self.finais:
                        if transicao not in aux:
                            aux.append(transicao)
                    else:
                        vazia = 0

        return vazia

