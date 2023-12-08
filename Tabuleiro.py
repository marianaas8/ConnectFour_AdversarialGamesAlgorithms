import copy

class Puzzle:

    #construtor
    def __init__(self, arg, pai=None, depth=0, antigo=None):
        self.estado = arg
        self.encontra_coord()
        self.filhos = []
        self.recuar = pai
        self.profundidade = depth
        self.l_anterior = antigo

    #coloca '' entre cada valor e retorna o hash value dessa coisa
    def __hash__(self):
        return hash(''.join(self.estado))

    #guarda estado do tabuleiro fazendo uma cópia deste
    def __copy__(self):
        return Puzzle(self.estado)

    #.rjust(2, '0') --> "ajustar à direita" para não ficar desformatado
    #lê os valores de um ficheiro e coloca-os na forma de um tabuleiro
    def __str__(self):
        text = """┌──┬──┬──┬──┐
│{}│{}│{}│{}│
├──┼──┼──┼──┤
│{}│{}│{}│{}│
├──┼──┼──┼──┤
│{}│{}│{}│{}│
├──┼──┼──┼──┤
│{}│{}│{}│{}│
└──┴──┴──┴──┘""" \
            .format(self.estado[0].rjust(2, '0'), self.estado[1].rjust(2, '0'), self.estado[2].rjust(2, '0'),
                    self.estado[3].rjust(2, '0'),
                    self.estado[4].rjust(2, '0'), self.estado[5].rjust(2, '0'), self.estado[6].rjust(2, '0'),
                    self.estado[7].rjust(2, '0'),
                    self.estado[8].rjust(2, '0'), self.estado[9].rjust(2, '0'), self.estado[10].rjust(2, '0'),
                    self.estado[11].rjust(2, '0'),
                    self.estado[12].rjust(2, '0'), self.estado[13].rjust(2, '0'), self.estado[14].rjust(2, '0'),
                    self.estado[15].rjust(2, '0')).replace("00", "  ")
        return text

    #verificar se são iguais
    def __eq__(self, other):
        return self.estado == other

    #encontra as coordenadas do ponto
    def encontra_coord(self):
        i = 0
        while self.estado[i] != '0':
            i += 1
        self.x, self.y = (int(i / 4), i % 4)

    def coord(self):
        return self.x, self.y

     # Definicao dos movimentos do Zero
    def zero_esquerda(self):
        move = copy.deepcopy(self.estado)
        anterior = copy.deepcopy(self.recuar)
        antes = copy.deepcopy(self.l_anterior)
        if antes is None:
            antes = [self.estado]
        else:
            antes.append(self.estado)
        if anterior is None:
            anterior = ['Esquerda']
        else:
            anterior.append('Esquerda')
        if self.y != 0:
            move[self.x * 4 + self.y] = move[self.x * 4 + self.y - 1]
            move[self.x * 4 + self.y - 1] = '0'
            tleft = Puzzle(move, pai=anterior, depth=self.profundidade + 1, antigo = antes)
            self.filhos.append(tleft)

    def zero_direita(self):
        move = copy.deepcopy(self.estado)
        anterior = copy.deepcopy(self.recuar)
        antes = copy.deepcopy(self.l_anterior)
        if antes is None:
            antes = [self.estado]
        else:
            antes.append(self.estado)
        if anterior is None:
            anterior = ['Direita']
        else:
            anterior.append('Direita')
        if self.y != 3:
            move[self.x * 4 + self.y] = move[self.x * 4 + self.y + 1]
            move[self.x * 4 + self.y + 1] = '0'
            tright = Puzzle(move, pai=anterior, depth=self.profundidade + 1, antigo = antes)
            self.filhos.append(tright)

    def zero_cima(self):
        move = copy.deepcopy(self.estado)
        anterior = copy.deepcopy(self.recuar)
        antes = copy.deepcopy(self.l_anterior)
        if antes is None:
            antes = [self.estado]
        else:
            antes.append(self.estado)
        if anterior is None:
            anterior = ['Cima']
        else:
            anterior.append('Cima')
        if self.x != 0:
            move[self.x * 4 + self.y] = move[(self.x - 1) * 4 + self.y]
            move[(self.x - 1) * 4 + self.y] = '0'
            tup = Puzzle(move, pai=anterior, depth=self.profundidade + 1, antigo = antes)
            self.filhos.append(tup)

    def zero_baixo(self):
        move = copy.deepcopy(self.estado)
        anterior = copy.deepcopy(self.recuar)
        antes = copy.deepcopy(self.l_anterior)
        if antes is None:
            antes = [self.estado]
        else:
            antes.append(self.estado)
        if anterior is None:
            anterior = ['Baixo']
        else:
            anterior.append('Baixo')
        if self.x != 3:
            move[self.x * 4 + self.y] = move[(self.x + 1) * 4 + self.y]
            move[(self.x + 1) * 4 + self.y] = '0'
            tdown = Puzzle(move, pai=anterior, depth=self.profundidade + 1, antigo = antes)
            self.filhos.append(tdown)

    def movimentos(self):
        if self.profundidade > 1:
            ultimo = self.recuar[self.profundidade-1]
        else:
            ultimo = "0"
        if ultimo != "Direita":
            self.zero_esquerda()
        if ultimo != "Esquerda":
            self.zero_direita()
        if ultimo != "Baixo":
            self.zero_cima()
        if ultimo != "Cima":
            self.zero_baixo()
        return self.filhos

    def __iter__(self):
        return iter(self.estado)
