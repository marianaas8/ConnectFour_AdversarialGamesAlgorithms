from collections import deque

class MinHeap:
    def __init__(self, estado_final, c):
        self.dados = [None]
        self.tamanho = 0
        self.comparador = c
        self.estado_final = estado_final

    def __len__(self):
        return self.tamanho

    def __contains__(self, item):
        return item in self.dados

    def __str__(self):
        return str(self.dados)

    def compara(self, x, y):
        x = self.comparador(self.dados[x], self.estado_final)
        y = self.comparador(self.dados[y], self.estado_final)

        if x < y:
            return True
        else:
            return False

    def posicao(self, x):
        for i in range(self.tamanho+1):
            if x == self.dados[i]:
                return i
        return None

    def up(self, i):
        while i > 1 and self.compara(i, int(i/2)):
            self.swap(i, int(i/2))
            i = int(i/2)

    def down(self, i):
        tamanho = self.tamanho
        while 2*i <= tamanho:
            j = 2*i
            if j < tamanho and self.compara(j+1, j):
                j += 1
            if self.compara(i, j):
                break
            self.swap(i, j)
            i = j

    def swap(self, i, j):
        t = self.dados[i]
        self.dados[i] = self.dados[j]
        self.dados[j] = t

    def push(self, x):
        self.tamanho += 1
        self.dados.append(x)
        self.up(self.tamanho)

    def pop(self):
        if self.tamanho < 1:
            return None
        t = self.dados[1]
        self.dados[1] = self.dados[self.tamanho]
        self.dados[self.tamanho] = t
        self.tamanho -= 1
        self.down(1)
        self.dados.pop()
        return t


def bfs(estado_inicial, estado_final):
    total_nos = 1
    fronteira = deque()
    fronteira.append(estado_inicial)

    while len(fronteira) > 0:
        estado = fronteira.popleft()

        if estado_final == estado:
            return estado.l_anterior, estado.recuar, total_nos
        for vizinho in estado.movimentos():
            total_nos += 1
            fronteira.append(vizinho)
        del(estado);
    return False, False, total_nos

def dfs(estado_inicial, estado_final, profundidade):
    total_nos = 1
    fronteira = list()
    visitados = set()
    fronteira.append(estado_inicial)

    while len(fronteira) > 0:
        estado = fronteira.pop()
        visitados.add(estado)

        if estado == estado_final:
            return estado.l_anterior, estado.recuar, total_nos

        for vizinho in estado.movimentos():
            total_nos += 1
            if vizinho.profundidade <= profundidade:
                if vizinho not in visitados or vizinho not in fronteira:
                    fronteira.append(vizinho)
        del(estado)
    return False, False, total_nos

def idfs(estado_inicial, estado_final, profundidade):
    total_nos = 0
    for i in range(0, profundidade+1):
        estados, resultado, nos = dfs(estado_inicial, estado_final, i)
        total_nos += nos
        if (resultado):
            return estados, resultado, total_nos
    return False, False, total_nos

def astar(estado_inicial, estado_final, heuristica):
    total_nos = 1
    fronteira = MinHeap(estado_final, heuristica)
    fronteira.push(estado_inicial)
    visitados = set()

    while len(fronteira) > 0:
        estado = fronteira.pop()
        visitados.add(estado)

        if estado_final == estado:
            return estado.l_anterior, estado.recuar, total_nos

        for vizinho in estado.movimentos():
            total_nos += 1
            if vizinho not in fronteira and vizinho not in visitados:
                fronteira.push(vizinho)
            elif vizinho in fronteira:
                i = fronteira.posicao(vizinho)
                if fronteira.dados[i].profundidade > vizinho.profundidade:
                    fronteira.dados[i] = vizinho
                    fronteira.up(i)

    return False, False, total_nos


def greedy(estado_inicial, estado_final, heuristica):
    total_nos = 1
    visitados = set()
    fronteira = MinHeap(estado_final, heuristica)
    fronteira.push(estado_inicial)

    while len(fronteira) > 0:
        estado = fronteira.pop()
        visitados.add(estado)

        if estado_final == estado:
            return estado.l_anterior, estado.recuar, total_nos

        for vizinho in estado.movimentos():
            total_nos += 1
            if vizinho not in visitados:
                fronteira.push(vizinho)
    return False, False, total_nos


def misplaced(estado_inicial, estado_final):
    inicial = estado_inicial.estado
    objetivo = estado_final.estado
    profundidade = estado_inicial.profundidade
    soma = 0
    for x, y in zip(objetivo, inicial):
        if x != y and x != '0':
            soma += 1
    return soma + profundidade

def manhattan(estado_inicial, estado_final):
    inicial = estado_inicial.estado
    objetivo = estado_final.estado
    profundidade = estado_inicial.profundidade
    soma = 0
    for i in range(16):
        if objetivo[i] == '0':
            continue
        x1, y1 = (int(i / 4), i % 4)
        for j in range(16):
            if objetivo[i] == inicial[j]:
                x2, y2 = (int(j / 4), j % 4)
                soma += abs(x1 - x2) + abs(y1 - y2)
                break
    return soma + profundidade
