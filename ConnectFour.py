import math
import time
import random
import copy
from os import system
import sys, pygame
import psutil
pygame.init()

#Classe para os nós da árvore Monte Carlo
class Node:
    def __init__(self, move, pai):
        self.move = move
        self.pai = pai
        self.N = 0   #simulações
        self.Q = 0   #pontuação
        self.filhos = {}

    #adiciona os filhos a um nó
    def adiciona_filhos(self, filhos):
        for filho in filhos:
            self.filhos[filho.move] = filho

    #função Upper Confidence Bound (UCB)
    def UCB(self):
        if self.N == 0:
            return float('inf')
        return self.Q / self.N + math.sqrt(2) * math.sqrt(math.log(self.pai.N) / self.N)

#Classe para Monte Carlo
class MCTS:
    def __init__(self, tabuleiro, jog):
        self.estado_raiz = Metodos.copia(tabuleiro)
        self.raiz = Node(None, None)
        self.jog = jog

    #função seleção
    def selection(self):
        node = self.raiz
        tabuleiro = Metodos.copia(self.estado_raiz)

        while len(node.filhos) != 0:
            filhos = node.filhos.values()
            maior_ucb = max(filhos, key=lambda n: n.UCB()).UCB()
            max_nodes = [n for n in filhos if n.UCB() == maior_ucb]
            node = random.choice(max_nodes)
            px = node.move
            py = Metodos.vazios[px]
            tabuleiro[py][px] = self.jog

            if node.N == 0:
                return node, tabuleiro

        if self.expand(node, tabuleiro):
            node = random.choice(list(node.filhos.values()))
            px = node.move
            py = Metodos.vazios[px]
            tabuleiro[py][px] = self.jog

        return node, tabuleiro

    #função expansão
    def expand(self, pai: Node, tabuleiro) -> bool:
        if Metodos.fim_jogo(tabuleiro, self.jog) != -1 or len(Metodos.jogadas_possiveis(tabuleiro))==0:
            return False

        filhos = [Node(move, pai) for move in Metodos.jogadas_possiveis(tabuleiro)]
        pai.adiciona_filhos(filhos)

        return True

    #função simulação até um limite de jogadas
    def simulation(self, tabuleiro, num_jogadas):
        for i in range(num_jogadas):
            if Metodos.fim_jogo(tabuleiro, self.jog) != -1 or len(Metodos.jogadas_possiveis(tabuleiro)) == 0:
                break
            px = random.choice(Metodos.jogadas_possiveis(tabuleiro))
            py = Metodos.vazios[px]
            tabuleiro[py][px] = self.jog
        recompensa = Metodos.conta_pontos(tabuleiro, self.jog)
        return recompensa

    #função retropropagação
    def back_propagate(self, node, recompensa):
        while node is not None:
            node.N += 1
            node.Q += recompensa
            node = node.pai

    #faz a pesquisa utilizando os 4 passos
    def search(self, dificuldade):
        num_jogadas = 100*dificuldade
        node, tabuleiro = self.selection()
        recompensa = self.simulation(tabuleiro, num_jogadas)
        self.back_propagate(node, recompensa)


    #Retorna o melhor movimento tendo em conta o ucb
    def best_move(self):
        if Metodos.fim_jogo(self.estado_raiz, self.jog) != -1:
            return -1

        maior_ucb = max(self.raiz.filhos.values(), key=lambda n: n.N).N
        max_nodes = [n for n in self.raiz.filhos.values() if n.N == maior_ucb]
        melhor_filho = random.choice(max_nodes)

        return melhor_filho.move

#Constantes utilizadas
class Constantes:
    BLACK = (0,0,0)
    WHITE = (255,255,255)
    RED = (255,0,0)
    GREEN = (0,255,0)
    YELLOW = (255,255,0)
    BLUE = (0,0,255)

#Operadores
class movimento:
    def __init__(self, x = 0, y = 0, jog = 0):
        self.x = x #coordenadas
        self.y = y
        self.jog = jog

#Estado do Jogo/Tabuleiro
class Metodos:
    nMovs = 0
    vazios = [5,5,5,5,5,5,5]
    screen = pygame.Surface((0,0))
    sq = (math.trunc(700 / float(7)))

    #Faz a cópia de um tabuleiro
    @staticmethod
    def copia(tabuleiro):
       return copy.deepcopy(tabuleiro)


    # Dado o jogador atual retorna o outro jogador
    @staticmethod
    def outroJog(jog):
        if jog == 1:
            return 2
        else:
            return 1

    # Assinala (ou desassinala tipo=0) circulos a branco
    @staticmethod
    def assinala(tabuleiro, tipo):
        cor = Constantes.BLACK
        if tipo == 1:
            cor = Constantes.WHITE
        for i in range (7):
            pygame.draw.circle(Metodos.screen, cor, (i*Metodos.sq+Metodos.sq/2, Metodos.vazios[i]*Metodos.sq+Metodos.sq/2), (Metodos.sq/2) - 2, 2)

    # Mostra o tabuleiro em modo grafico
    @staticmethod
    def mostra_tabul(tabuleiro):
        cor = Constantes.BLUE
        pygame.draw.rect(Metodos.screen, cor, pygame.Rect(0, 0, 700, 600))
        i = 0
        while i<6:
            j = 0
            while j<7:
                cor = Constantes.BLACK
                pygame.draw.circle(Metodos.screen, cor, (j*Metodos.sq+Metodos.sq/2, i*Metodos.sq+Metodos.sq/2), (Metodos.sq/2) - 2) #circulos em preto (Disponiveis)
                if tabuleiro[i][j] == 1 or tabuleiro[i][j] == 2:
                    if tabuleiro[i][j] == 1:
                        cor = Constantes.YELLOW
                    else:
                        cor = Constantes.RED
                    pygame.draw.circle(Metodos.screen, cor, (j*Metodos.sq+Metodos.sq/2, i*Metodos.sq+Metodos.sq/2), (Metodos.sq/2) - 2) #peca
                j += 1
            i += 1

    # Pede ao utlizador que escolha um dos modos de jogo possíveis
    @staticmethod
    def tipo():
        return int(input("Jogo Connect Four\nEscolha o modo de jogo: \n1-Hum/Hum, 2-Hum/Computador, 3-Computador/Hum, 4-Computador/Computador\n"))

    # Pede ao utlizador que escolha uma das estrategias de jogo possíveis
    @staticmethod
    def tipo_jogo(jog):
        return int(input("\nEscolha a estratégia do jogador %d: \n1-Minimax, 2-Alfa-Beta, 3-MonteCarlo\n" %jog))

    # Pede ao utilizador que escolha a dificuldade do jogo
    @staticmethod
    def dificuldade(jog):
        return int(input("\nEscolha a dificuldade do jogador " + str(jog) + ": \n1-Fácil, 2-Intermédio, 3-Díficil\n")) #caso se tenha escolhido a opção 2, 3 ou 4


    # Finaliza o jogo indicando quem venceu ou se foi empate
    @staticmethod
    def finaliza(venc):
        Metodos.screen.fill(Constantes.BLACK)
        pygame.display.update()
        font = pygame.font.SysFont(None, 24)
        img = pygame.Surface((0,0))

        if venc == 0:
            print("Empate!!!\n")
            img = font.render("Empate!!!\n", True, Constantes.GREEN)
        elif venc == 1:
            print("Venceu o Jogador 1 - Amarelo!")
            img = font.render("Venceu o Jogador 1 - Amarelo!", True, Constantes.YELLOW)
        else:
            print("Venceu o Jogador 2 - Vermelho!")
            img = font.render("Venceu o Jogador 2 - Vermelho!", True, Constantes.RED)
        Metodos.screen.blit(img, (700/2-100, 700/2))
        pygame.display.update()

    # Indica se (x,y) está dentro do tabuleiro
    @staticmethod
    def dentro(x, y):
        return (x>=0 and x<=7-1 and y>=0 and y<=6-1)

    #indica se mov é um movimento valido
    @staticmethod
    def movimento_valido(mov):
        if not Metodos.dentro(mov.x, mov.y):
            return False #fora do tabuleiro
        if Metodos.vazios[mov.x]==mov.y:
            return True
        return False

    #Heurística
    def conta_pontos(tabuleiro, jogador):
        total_pontos = 0

        # Verifica se houve vitória
        if Metodos.fim_jogo(tabuleiro, jogador) != -1:
            if Metodos.fim_jogo(tabuleiro, jogador) == jogador:
                return 512
            elif Metodos.fim_jogo(tabuleiro, jogador) == Metodos.outroJog(jogador):
                return -512
            else:
                return 0

        # avalia segmentos na horizontal
        for linha in tabuleiro:
            for i in range(0, 4):
                segmento = linha[i:i+4]
                total_pontos += Metodos.avaliar_segmento(segmento, jogador)

        # avalia segmentos na vertical
        for coluna in range(0, 7):
            for i in range(0, 3):
                segmento = [tabuleiro[i][coluna], tabuleiro[i+1][coluna], tabuleiro[i+2][coluna], tabuleiro[i+3][coluna]]
                total_pontos += Metodos.avaliar_segmento(segmento, jogador)

        # avalia segmentos na diagonal \
        for i in range(0, 4):
            for j in range(0, 3):
                segmento = [tabuleiro[j][i], tabuleiro[j+1][i+1], tabuleiro[j+2][i+2], tabuleiro[j+3][i+3]]
                total_pontos += Metodos.avaliar_segmento(segmento, jogador)

        # avalia segmentos na diagonal /
        for i in range(0, 4):
            for j in range(3, 6):
                segmento = [tabuleiro[j][i], tabuleiro[j-1][i+1], tabuleiro[j-2][i+2], tabuleiro[j-3][i+3]]
                total_pontos += Metodos.avaliar_segmento(segmento, jogador)

        return total_pontos

    #Função de avaliação
    def avaliar_segmento(segmento, jogador):
        contador_jogador = segmento.count(jogador)
        contador_adversario = segmento.count(Metodos.outroJog(jogador))
        if contador_adversario == 0:
            if contador_jogador == 3:
                return +50
            elif contador_jogador == 2:
                return +10
            elif contador_jogador == 1:
                return +1
            else:
                return 0
        elif contador_jogador == 0:
            if contador_adversario == 3:
                return -50
            elif contador_adversario == 2:
                return -10
            elif contador_adversario == 1:
                return -1
            else:
                return 0
        else:
            return 0

    #Determina se o jogador ainda tem jogadas válidas
    @staticmethod
    def jogadas_validas():
        for i in range(7):
            if Metodos.vazios[i]!=-1:
                return True
        return False

    #retorna a lista com as posições possiveis em que se pode jogar
    def jogadas_possiveis(tabuleiro):
        lista = []
        for posicao in range(7):
            if tabuleiro[0][posicao] == 0:
                lista.append(posicao)
        return lista

    # Verificar se o jogo terminou retornando o vencedor
    @staticmethod
    def fim_jogo(tabuleiro, jog):

        contador_amarelos = 0
        contador_vermelhos = 0

        #verifica slots na horizontal
        for c in range(7):
            for i in range(4):
                for j in range(i,i+4):
                    if tabuleiro[c][j]==1:
                        contador_amarelos += 1
                    elif tabuleiro[c][j]==2:
                        contador_vermelhos += 1
                if contador_amarelos == 4:
                    return 1
                elif contador_vermelhos == 4:
                    return 2
                contador_amarelos = 0
                contador_vermelhos = 0

        #verifica slots na vertical
        for c in range(7):
            for i in range(4):
                for j in range(i,i+4):
                    if tabuleiro[j][c]==1:
                        contador_amarelos += 1
                    elif tabuleiro[j][c]==2:
                        contador_vermelhos += 1
                if contador_amarelos == 4:
                    return 1
                elif contador_vermelhos == 4:
                    return 2
                contador_amarelos = 0
                contador_vermelhos = 0

        #verifica slots na diagonal (/)
        for i in range(3,7):
            for j in range(4):
                c = i
                d = j

                while c != i-4 and d!=j+4:
                    if tabuleiro[c][d]==1:
                        contador_amarelos += 1
                    elif tabuleiro[c][d]==2:
                        contador_vermelhos += 1
                    c -= 1
                    d += 1
                if contador_amarelos == 4:
                    return 1
                elif contador_vermelhos == 4:
                    return 2
                contador_amarelos = 0
                contador_vermelhos = 0

        #verifica slots na diagonal (\)
        for i in range(0,3):
            for j in range(4):
                c = i
                d = j

                while c != i+4 and d!=j+4:
                    if tabuleiro[c][d]==1:
                        contador_amarelos += 1
                    elif tabuleiro[c][d]==2:
                        contador_vermelhos += 1
                    c += 1
                    d += 1
                if contador_amarelos == 4:
                    return 1
                elif contador_vermelhos == 4:
                    return 2
                contador_amarelos = 0
                contador_vermelhos = 0

        if Metodos.jogadas_validas():
            return -1 #ainda existem jogadas
        return 0 #empate

    # Jogada do Humano
    @staticmethod
    def jogada_Humano(tabuleiro, jog):
        mov = movimento(0,0,jog)
        px = 0
        py = 0
        condition = True
        while condition:
            pygame.event.get()
            pos = pygame.mouse.get_pos()
            px = math.trunc(pos[0]/Metodos.sq) # coordenadas onde se carregou
            py = math.trunc(pos[1]/Metodos.sq)
            Metodos.assinala(tabuleiro,1)
            mov = movimento(px,py,jog)
            if pygame.mouse.get_pressed()[0] and Metodos.movimento_valido(mov):
                tabuleiro[py][px] = jog
                Metodos.vazios[px] -= 1
                condition = False
            pygame.display.update()
            time.sleep(0.1)

    #jogada minimax
    def jogada_pc_minimax(tabuleiro, jog, dificuldade):
        bestmov = movimento()
        bestmov = Metodos.minimax(jog, tabuleiro, dificuldade)
        if bestmov is not None:
            tabuleiro[Metodos.vazios[bestmov]][bestmov] = jog
            Metodos.vazios[bestmov] -= 1

    #retorna a melhor jogada possível com minimax
    def minimax(jog, tabuleiro, dificuldade):
        _ , move = Metodos.maximo(jog, tabuleiro, dificuldade, None)
        return move

    #função maximo para o minimax
    def maximo(jog, tabuleiro, dificuldade, move):
        if Metodos.fim_jogo(tabuleiro, jog)!=-1 or dificuldade==0:
            tabuleiro_cp = Metodos.copia(tabuleiro)
            py = Metodos.vazios[move]
            tabuleiro_cp[py][move] = jog
            return Metodos.conta_pontos(tabuleiro_cp, jog),move

        max_value = float("-inf")
        for s in Metodos.jogadas_possiveis(tabuleiro):
            tabuleiro_cp = Metodos.copia(tabuleiro)
            py = Metodos.vazios[s]
            tabuleiro_cp[py][s] = jog
            value, _ = Metodos.minimo(jog, tabuleiro_cp, dificuldade - 1, s)
            if  value>max_value:
                max_value=value
                move=s

        return max_value,move

    #função minimo para o minimax
    def minimo(jog, tabuleiro, dificuldade, move):
        if Metodos.fim_jogo(tabuleiro, jog)!=-1 or dificuldade==0:
            tabuleiro_cp = Metodos.copia(tabuleiro)
            py = Metodos.vazios[move]
            tabuleiro_cp[py][move] = jog
            return Metodos.conta_pontos(tabuleiro_cp, jog),move

        min_value = float("inf")
        for s in Metodos.jogadas_possiveis(tabuleiro):
            tabuleiro_cp = Metodos.copia(tabuleiro)
            py = Metodos.vazios[s]
            tabuleiro_cp[py][s] = jog
            value, _ = Metodos.maximo(jog, tabuleiro_cp, dificuldade - 1, s)
            if value<min_value:
                min_value=value
                move = s

        return min_value,move

    #jogada minimax com corte alfa-beta
    def jogada_pc_alphabeta(tabuleiro, jog, dificuldade):
        bestmov = Metodos.alphabeta(jog, Metodos.copia(tabuleiro), dificuldade)
        if bestmov is not None:
            tabuleiro[Metodos.vazios[bestmov]][bestmov] = jog
            Metodos.vazios[bestmov] -= 1

    #retorna a melhor jogada possível com minimax com cortes alfa-beta
    def alphabeta(jog, tabuleiro, dificuldade):
        alfa = float("-inf")
        beta = float("inf")
        _ , move = Metodos.maximo_alphabeta(jog, tabuleiro, dificuldade, alfa, beta, None)
        return move

    #função maximo para o minimax com cortes alfa-beta
    def maximo_alphabeta(jog, tabuleiro, dificuldade, alfa, beta, move):
        if Metodos.fim_jogo(tabuleiro, jog)!=-1 or dificuldade==0:
            tabuleiro_cp = Metodos.copia(tabuleiro)
            py = Metodos.vazios[move]
            tabuleiro_cp[py][move] = jog
            return Metodos.conta_pontos(tabuleiro_cp, jog),move

        max_value = float("-inf")
        for s in Metodos.jogadas_possiveis(tabuleiro):
            tabuleiro_cp = Metodos.copia(tabuleiro)
            py = Metodos.vazios[s]
            tabuleiro_cp[py][s] = jog
            value, _ = Metodos.minimo_alphabeta(jog, tabuleiro_cp, dificuldade - 1, alfa, beta, s)
            if  value>max_value:
                max_value=value
                move=s
            alfa = max(alfa, max_value)
            if alfa >= beta:
                break

        return max_value,move

    #função minimo para o minimax com cortes alfa-beta
    def minimo_alphabeta(jog, tabuleiro, dificuldade, alfa, beta, move):
        if Metodos.fim_jogo(tabuleiro, jog)!=-1 or dificuldade==0:
            tabuleiro_cp = Metodos.copia(tabuleiro)
            py = Metodos.vazios[move]
            tabuleiro_cp[py][move] = jog
            return Metodos.conta_pontos(tabuleiro_cp, jog),move

        min_value = float("inf")
        for s in Metodos.jogadas_possiveis(tabuleiro):
            tabuleiro_cp = Metodos.copia(tabuleiro)
            py = Metodos.vazios[s]
            tabuleiro_cp[py][s] = jog
            value, _ = Metodos.maximo_alphabeta(jog, tabuleiro_cp, dificuldade - 1, alfa, beta, s)
            if value<min_value:
                min_value=value
                move = s
            beta = min(beta, min_value)
            if beta <= alfa:
                break

        return min_value,move

    #Jogada Monte Carlo
    @staticmethod
    def jogada_pc_montecarlo(tabuleiro, jog, dificuldade):
        mcts = MCTS(tabuleiro, jog)
        mcts.search(dificuldade)
        bestmov = mcts.best_move()
        tabuleiro[Metodos.vazios[bestmov]][bestmov] = jog
        Metodos.vazios[bestmov] -= 1


    # Dependendo do modo de jogo e do numero da jogada pede uma jogada ao humano ou calcula uma jogada para o PC
    def jogada(tabuleiro, n, jog, tJog, estrategia, dificuldade1, dificuldade2):
        if math.fmod(n, 2) == 1: #jogador 1
            if tJog==1 or tJog==2:
                Metodos.jogada_Humano(tabuleiro, jog)
            elif estrategia==1:
                Metodos.jogada_pc_minimax(tabuleiro, jog, dificuldade1)
            elif estrategia==2:
                Metodos.jogada_pc_alphabeta(tabuleiro, jog, dificuldade1)
            else:
                Metodos.jogada_pc_montecarlo(tabuleiro, jog, dificuldade1)
        else: #jogador 2
            if tJog == 1 or tJog == 3:
                Metodos.jogada_Humano(tabuleiro, jog)
            elif estrategia==1:
                Metodos.jogada_pc_minimax(tabuleiro, jog, dificuldade2)
            elif estrategia==2:
                Metodos.jogada_pc_alphabeta(tabuleiro, jog, dificuldade2)
            else:
                Metodos.jogada_pc_montecarlo(tabuleiro, jog, dificuldade2)

# Função principal
def main():
    fim = -1
    jog = 0

    Metodos.screen = pygame.display.set_mode((700,600))
    pygame.display.set_caption ('Connect Four')
    tabuleiro = [[0,0,0,0,0,0,0], [0,0,0,0,0,0,0], [0,0,0,0,0,0,0], [0,0,0,0,0,0,0], [0,0,0,0,0,0,0], [0,0,0,0,0,0,0], [0,0,0,0,0,0,0]] # tabuleiro: 0-vazio, 1-peça jog1, 2-peça jog2, 8-impossivel
    while  True:
        Metodos.nMovs = 0
        tipo = Metodos.tipo()
        dificuldade1 = 0
        dificuldade2 = 0
        estrategia = 0
        if tipo==3 or tipo==4:
            estrategia = Metodos.tipo_jogo(1)
            dificuldade1 = Metodos.dificuldade(1)
        if tipo==2 or tipo==4:
            estrategia = Metodos.tipo_jogo(2)
            dificuldade2 = Metodos.dificuldade(2)

        condition = True
        inicio = time.time()
        while condition:
            Metodos.nMovs += 1
            jog = Metodos.outroJog(jog) # incrementa jogada e troca de jogador
            Metodos.mostra_tabul(tabuleiro) # mostra o tabuleiro no ecrã

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            pygame.display.update()
            Metodos.jogada(tabuleiro, Metodos.nMovs, jog, tipo, estrategia, dificuldade1, dificuldade2) # executa jogada Humano/PC
            print("Connect Four - Jogada Nº: {0:d}  Jogador: {1:d}, Avaliação: ".format(Metodos.nMovs, jog), Metodos.conta_pontos(tabuleiro, 1), Metodos.conta_pontos(tabuleiro, 2))
            fim = Metodos.fim_jogo(tabuleiro, jog) # verifica se o jogo acabou
            condition = fim == -1
        #Mostrar estado final do jogo
        Metodos.mostra_tabul(tabuleiro)
        pygame.display.update()
        time.sleep(1) # 1 segundo
        #Mostrar vencedor
        Metodos.finaliza(fim) # mostra quem venceu o jogo
        fim = time.time()
        tempo = fim - inicio
        print("Tempo de execução: %f segundos" %tempo)
        print('Percentagem de CPU utilizada:', psutil.cpu_percent(), '%')
        print('Percentagem de memória RAM utilizada:', psutil.virtual_memory()[2], '%')
        time.sleep(2)
        sys.exit()

if __name__ == "__main__":
    main()
