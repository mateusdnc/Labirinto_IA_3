import numpy as np
import random as rd


class No(object):
    def __init__(self, pai=None, estado=None, valor1=None,
                 valor2=None, anterior=None, proximo=None):
        # controle da árvore de busca
        self.pai = pai
        # indica o nó do grafo
        self.estado = estado
        # função de avaliação f(n) do método
        self.valor1 = valor1
        # custo do caminho da origem até o nó atual
        self.valor2 = valor2
        # controle da lista encadeada
        self.anterior = anterior
        self.proximo = proximo


class lista(object):
    head = None
    tail = None

    # INSERE NO INÍCIO DA LISTA
    def inserePrimeiro(self, s, v1, v2, p):
        novo_no = No(p, s, v1, v2, None, None)
        if self.head == None:
            self.tail = novo_no
        else:
            novo_no.proximo = self.head
            self.head.anterior = novo_no
        self.head = novo_no

    # INSERE NO FIM DA LISTA
    def insereUltimo(self, s, v1, v2, p):

        novo_no = No(p, s, v1, v2, None, None)

        if self.head is None:
            self.head = novo_no
        else:
            self.tail.proximo = novo_no
            novo_no.anterior = self.tail
        self.tail = novo_no

    # INSERE NO FIM DA LISTA
    def inserePos_X(self, s, v1, v2, p):

        # se lista estiver vazia
        if self.head is None:
            self.inserePrimeiro(s, v1, v2, p)
        else:
            atual = self.head
            while atual.valor1 < v1:
                atual = atual.proximo
                if atual is None:
                    break

            if atual == self.head:
                self.inserePrimeiro(s, v1, v2, p)
            else:
                if atual is None:
                    self.insereUltimo(s, v1, v2, p)
                else:
                    novo_no = No(p, s, v1, v2, None, None)
                    aux = atual.anterior
                    aux.proximo = novo_no
                    novo_no.anterior = aux
                    atual.anterior = novo_no
                    novo_no.proximo = atual

    # REMOVE NO INÍCIO DA LISTA

    def deletaPrimeiro(self):
        if self.head is None:
            return None
        else:
            no = self.head
            self.head = self.head.proximo
            if self.head is not None:
                self.head.anterior = None
            else:
                self.tail = None
            return no

    # REMOVE NO FIM DA LISTA
    def deletaUltimo(self):
        if self.tail is None:
            return None
        else:
            no = self.tail
            self.tail = self.tail.anterior
            if self.tail is not None:
                self.tail.proximo = None
            else:
                self.head = None
            return no

    def vazio(self):
        if self.head is None:
            return True
        else:
            return False

    def exibeLista(self):

        aux = self.head
        str = []
        while aux != None:
            linha = []
            linha.append(aux.estado)
            linha.append(aux.valor1)
            str.append(linha)
            aux = aux.proximo

        return str

    def exibeArvore(self):

        atual = self.tail
        caminho = []
        while atual.pai is not None:
            caminho.append(atual.estado)
            atual = atual.pai
        caminho.append(atual.estado)
        return caminho

    def exibeArvore1(self, s):

        atual = self.head
        while atual.estado != s:
            atual = atual.proximo

        caminho = []
        atual = atual.pai
        while atual.pai is not None:
            caminho.append(atual.estado)
            atual = atual.pai
        caminho.append(atual.estado)
        return caminho

    def exibeArvore2(self, s, v1):

        atual = self.tail

        while atual.estado != s or atual.valor1 != v1:
            atual = atual.anterior

        caminho = []
        while atual.pai is not None:
            caminho.append(atual.estado)
            atual = atual.pai
        caminho.append(atual.estado)
        return caminho

    def primeiro(self):
        return self.head

    def ultimo(self):
        return self.tail


def convertAndSetMatrixToGraph(matriz):
    nosLocal = []  # Lista de IDs dos nós
    grafosLocal = []  # Lista de arestas para representar o grafo

    rows = len(matriz)
    cols = len(matriz[0])

    # Crie os nós e inicialize o grafo
    for i in range(rows):
        for j in range(cols):
            no_id = i * cols + j  # Gere IDs incrementais
            nosLocal.append(no_id)
            conexoes = []

            # Verifique as direções possíveis com base na posição
            if j < cols - 1:  # Direita
                conexoes.append((no_id + 1, matriz[i][j + 1]))
            if j > 0:  # Esquerda
                conexoes.append((no_id - 1, matriz[i][j - 1]))
            if i < rows - 1:  # Abaixo
                conexoes.append((no_id + cols, matriz[i + 1][j]))
            if i > 0:  # Acima
                conexoes.append((no_id - cols, matriz[i - 1][j]))

            grafosLocal.append(conexoes)

    return grafosLocal, nosLocal


def gera_H(grafo,nos,h,n, nosLocal, matriz):
    aux = busca()
    h = np.zeros((n, n), int)
    i = 0
    for no_origem in nosLocal:
        j = 0
        for no_destino in nosLocal:
            if no_origem != no_destino:
                cam, v = aux.custo_uniforme(grafo,nos,h, no_origem, no_destino)
                ale = rd.uniform(0, 1)
                while(ale < 0.8) :
                    ale = rd.uniform(0, 1)
                h[i][j] = v*rd.uniform(0, 1)
            j += 1
        i += 1
    return h


class busca(object):

    def custo_uniforme(self, grafo,nos,h,inicio, fim):
        # print("================================================")
        print("ALVO: "+str(fim))
        # print("")
        # print("\nGRAFO: "+str(grafo))
        # print("================================================")

        l1 = lista()
        l2 = lista()
        visitado = []

        l1.insereUltimo(inicio, 0, 0, None)
        l2.insereUltimo(inicio, 0, 0, None)
        linha = []
        linha.append(inicio)
        linha.append(0)
        visitado.append(linha)

        while l1.vazio() == False:
            atual = l1.deletaPrimeiro()

            if atual.estado == fim:
                caminho = []
                caminho = l2.exibeArvore2(atual.estado, atual.valor1)
                # print("Cópia da árvore:\n", l2.exibeLista())
                # print("\nÁrvore de busca:\n", l1.exibeLista(), "\n")
                return caminho, atual.valor2

            ind = nos.index(atual.estado)
            for novo in grafo[ind]:

                # CÁLCULO DO CUSTO DA ORIGEM ATÉ O NÓ ATUAL
                v2 = atual.valor2 + novo[1]  # custo do caminho
                v1 = v2  # f1(n)

                flag1 = True
                flag2 = True
                for j in range(len(visitado)):
                    if visitado[j][0] == novo[0]:
                        if visitado[j][1] <= v2:
                            flag1 = False
                        else:
                            visitado[j][1] = v2
                            flag2 = False
                        break

                if flag1:
                    l1.inserePos_X(novo[0], v1, v2, atual)
                    # l2.inserePos_X(novo[0], v1, v2, atual)
                    l2.insereUltimo(novo[0], v1, v2, atual)
                    if flag2:
                        linha = []
                        linha.append(novo[0])
                        linha.append(v2)
                        visitado.append(linha)

        return "Caminho não encontrado"

    def greedy(grafo,nos,h,inicio, fim):
        ind_f = nos.index(fim)
        l1 = lista()
        l2 = lista()
        visitado = []

        l1.insereUltimo(inicio, 0, 0, None)
        l2.insereUltimo(inicio, 0, 0, None)
        linha = []
        linha.append(inicio)
        linha.append(0)
        visitado.append(linha)

        while l1.vazio() == False:
            atual = l1.deletaPrimeiro()

            if atual.estado == fim:
                caminho = []
                caminho = l2.exibeArvore2(atual.estado, atual.valor1)
                # print("Cópia da árvore:\n",l2.exibeLista())
                # print("\nÁrvore de busca:\n",l1.exibeLista(),"\n")

                return caminho, atual.valor2

            ind = nos.index(atual.estado)
            for novo in grafo[ind]:

                ind1 = nos.index(novo[0])

                # CÁLCULO DO CUSTO DA ORIGEM ATÉ O NÓ ATUAL
                v2 = atual.valor2 + novo[1]  # custo do caminho
                v1 = h[ind_f][ind1]  # f2(n)

                flag1 = True
                flag2 = True
                for j in range(len(visitado)):
                    if visitado[j][0] == novo[0]:
                        if visitado[j][1] <= v2:
                            flag1 = False
                        else:
                            visitado[j][1] = v2
                            flag2 = False
                        break

                if flag1:
                    l1.inserePos_X(novo[0], v1, v2, atual)
                    l2.inserePos_X(novo[0], v1, v2, atual)
                    if flag2:
                        linha = []
                        linha.append(novo[0])
                        linha.append(v2)
                        visitado.append(linha)

        return "Caminho não encontrado"

    def a_estrela(grafo,nos,h,inicio, fim):
        # h = gera_H(len(nos), nos, matriz)

        ind_f = nos.index(fim)
        l1 = lista()
        l2 = lista()
        visitado = []

        l1.insereUltimo(inicio, 0, 0, None)
        l2.insereUltimo(inicio, 0, 0, None)
        linha = []
        linha.append(inicio)
        linha.append(0)
        visitado.append(linha)

        while l1.vazio() == False:
            atual = l1.deletaPrimeiro()

            if atual.estado == fim:
                caminho = []
                caminho = l2.exibeArvore2(atual.estado, atual.valor1)
                # print("Cópia da árvore:\n",l2.exibeLista())
                # print("\nÁrvore de busca:\n",l1.exibeLista(),"\n")
                return caminho, atual.valor2

            ind = nos.index(atual.estado)
            for novo in grafo[ind]:

                ind1 = nos.index(novo[0])

                # CÁLCULO DO CUSTO DA ORIGEM ATÉ O NÓ ATUAL
                v2 = atual.valor2 + novo[1]  # custo do caminho
                v1 = v2 + h[ind_f][ind1]  # f2(n)

                flag1 = True
                flag2 = True
                for j in range(len(visitado)):
                    if visitado[j][0] == novo[0]:
                        if visitado[j][1] <= v2:
                            flag1 = False
                        else:
                            visitado[j][1] = v2
                            flag2 = False
                        break

                if flag1:
                    l1.inserePos_X(novo[0], v1, v2, atual)
                    l2.inserePos_X(novo[0], v1, v2, atual)
                    if flag2:
                        linha = []
                        linha.append(novo[0])
                        linha.append(v2)
                        visitado.append(linha)

        return "Caminho não encontrado"

    def aia_estrela(grafo,nos,h,inicio, fim):
        # h = gera_H(len(nos), nos, matriz)
        pi = nos.index(inicio)
        pf = nos.index(fim)
        limite = h[pi][pf]

        ind_f = nos.index(fim)
        while True:
            lim_exc = []
            l1 = lista()
            l2 = lista()
            visitado = []

            l1.insereUltimo(inicio, 0, 0, None)
            l2.insereUltimo(inicio, 0, 0, None)
            linha = []
            linha.append(inicio)
            linha.append(0)
            visitado.append(linha)

            # print("Limite: ",limite)
            while l1.vazio() == False:
                atual = l1.deletaPrimeiro()

                if atual.estado == fim:
                    caminho = []
                    caminho = l2.exibeArvore2(atual.estado, atual.valor1)
                    # print("Cópia da árvore:\n",l2.exibeLista())
                    # print("\nÁrvore de busca:\n",l1.exibeLista(),"\n")

                    return caminho, atual.valor2

                ind = nos.index(atual.estado)
                for novo in grafo[ind]:

                    ind1 = nos.index(novo[0])

                    # CÁLCULO DO CUSTO DA ORIGEM ATÉ O NÓ ATUAL
                    v2 = atual.valor2 + novo[1]  # custo do caminho
                    v1 = v2 + h[ind_f][ind1]  # f2(n)

                    if v1 <= limite:
                        flag1 = True
                        flag2 = True
                        for j in range(len(visitado)):
                            if visitado[j][0] == novo[0]:
                                if visitado[j][1] <= v2:
                                    flag1 = False
                                else:
                                    visitado[j][1] = v2
                                    flag2 = False
                                break

                        if flag1:
                            l1.inserePos_X(novo[0], v1, v2, atual)
                            l2.inserePos_X(novo[0], v1, v2, atual)
                            if flag2:
                                linha = []
                                linha.append(novo[0])
                                linha.append(v2)
                                visitado.append(linha)
                    else:
                        lim_exc.append(v1)
            limite = sum(lim_exc)/len(lim_exc)
