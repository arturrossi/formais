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


def concatena_estados_lista(lista):
    for item in lista:
        if len(item) > 1:
            retorna_maior(item)
            junta_estados = ''.join(item)
            lista.remove(item)
            lista.append([junta_estados])


class AFD:
    def __init__(self):
        self.inicial = ''
        self.finais = []
        self.dicionario_transicoes_afd = {}
        self.alfabeto = []
        self.estados_visitados = []

    def converter_afn_para_afd(self, afn):
        self.alfabeto = afn.alfabeto
        self.inicial = afn.inicial

        #adiciona q0 aos estados visitados
        self.estados_visitados.append(['q0'])

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
                            lista_aux.extend(afn.dicionario_transicoes_afn[(estados, simbolo)])
                    lista_final.extend(list(set(lista_aux).union(lista_aux)))
                    self.dicionario_transicoes_afd[(tuple(estado), simbolo)] = lista_final
                    if estado not in self.estados_visitados:
                        self.estados_visitados.append(lista_final)

        for estados in afn.finais:
            for estado in self.estados_visitados:
                if estados in estado:
                    self.finais.append(estado)


    #transforma estados de tamanho maior que 1 em apenas um só, concatenando-os, por exemplo [['q2'], ['q3']] em ['q2q3']
    def concatena_estados_transicoes(self):
        for item,value in self.dicionario_transicoes_afd.items():
            if len(value) > 1:
                retorna_maior(value)
                junta_estados = ''.join(value)
                self.dicionario_transicoes_afd[item] = [junta_estados]
            if len(item[0][0]) > 1:
                item_aux = list(item[0])
                retorna_maior(item_aux)
                junta_estados = ''.join(item_aux)
                self.dicionario_transicoes_afd[(junta_estados, item[1])] = self.dicionario_transicoes_afd.pop(item)

    def funcao_total(self):
        estado_aux = 'qaux'
        self.estados_visitados.append([estado_aux])
        for simbolos in self.alfabeto:
            self.dicionario_transicoes_afd[(estado_aux, simbolos)] = [estado_aux]

        lista_aux = []

        for item in self.dicionario_transicoes_afd.items():
            for simbolo in self.alfabeto:
                if self.dicionario_transicoes_afd.get((item[0][0], simbolo)) is None:
                    lista_aux.append([(item[0][0], simbolo, estado_aux)])

        for itens in lista_aux:
            self.dicionario_transicoes_afd[(itens[0][0], itens [0][1])] = [itens[0][2]]



    def minimizar_afd(self):
        self.concatena_estados_transicoes()
        concatena_estados_lista(self.estados_visitados)
        concatena_estados_lista(self.finais)
        self.funcao_total()

        #print(self.dicionario_transicoes_afd)
        #print(self.estados_visitados)
        #print(self.finais)

        tabela = {}

        for i,item in enumerate(self.estados_visitados):
            for item_2 in self.estados_visitados[i+1:]:
                tabela[(tuple(item), tuple(item_2))] = (item in self.finais) and (item_2 not in self.finais)

        print(tabela)

        flag = True


        #print(tabela)

        while flag:
            flag = False

            for i, item in enumerate(self.estados_visitados):
                for item_2 in self.estados_visitados[i+1:]:
                    if tabela[(tuple(item), tuple(item_2))]:
                        continue
                    for simbolo in self.alfabeto:
                        transicao1 = self.dicionario_transicoes_afd.get((item[0], simbolo))
                        transicao2 = self.dicionario_transicoes_afd.get((item_2[0], simbolo))
                        #print(item[0], simbolo, transicao1)
                        #print(item_2[0], simbolo, transicao2)
                        marca = tabela.get((tuple(transicao1), tuple(transicao2)))
                        #q2q3 deu false quando era o segundo parametro
                        if transicao1 != transicao2 and marca is not None:
                            #print(item, simbolo, transicao1, item_2, simbolo, transicao2, marca)
                            flag = flag or marca
                            tabela[(tuple(item), tuple(item_2))] = marca

                            if marca:
                                break
       #print(self.dicionario_transicoes_afd)
        print(tabela)