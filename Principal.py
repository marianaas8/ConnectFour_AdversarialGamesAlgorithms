import sys
import argparse
from Tabuleiro import Puzzle
from Estrategias import bfs, dfs, idfs, astar, greedy, misplaced, manhattan
import time
import psutil
import cProfile


# verificar a paridade da diferença entre as posições dos espaços em branco
def paridade(b_i, b_f):
    m_inicial= [[b_i[0],b_i[1],b_i[2],b_i[3]],
                [b_i[4],b_i[5],b_i[6],b_i[7]],
                [b_i[8],b_i[9],b_i[10],b_i[11]],
                [b_i[12],b_i[13],b_i[14],b_i[15]]]
    m_final= [[b_f[0],b_f[1],b_f[2],b_f[3]],
                [b_f[4],b_f[5],b_f[6],b_f[7]],
                [b_f[8],b_f[9],b_f[10],b_f[11]],
                [b_f[12],b_f[13],b_f[14],b_f[15]]]

    for i in range (4):
        for j in range (4):
            if m_inicial[i][j]=="0":
                zero_inicial=(i,j)
            if m_final[i][j]=="0":
                zero_final=(i,j)
    dif_brancos=abs(zero_final[0]-zero_inicial[0])+abs(zero_final[1]-zero_inicial[1])

    #verificar se é possível chegar à configuração "perfeita"
    p=["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","0"]#configuração perfeita
    contador1 = 0 #conta saltinhos
    for i in range (len(b_i)):
        if b_i[i]!=p[i]:
            j=i
            while b_i[j]!=p[i]:
                j+=1
            b_i[j]=b_i[i]
            b_i[i]=p[i]
            contador1 += 1

    if (dif_brancos%2==contador1%2):
        print("É possível chegar à configuração standard.")
        print()
    else:
        print("Não é possível chegar à configuração standard.")

    #verificar a paridade da diferença das posições da matriz inicial e da matriz final
    contador = 0 #conta saltinhos
    for i in range (len(b_i)):
        if b_i[i]!=b_f[i]:
            j=i
            while b_i[j]!=b_f[i]:
                j+=1
            b_i[j]=b_i[i]
            b_i[i]=b_f[i]
            contador += 1

    if (dif_brancos%2!=contador%2):
        print('Tabuleiro inválido.')
        sys.exit(1)

def main():
    # Argumentos da entrada do script
    parser = argparse.ArgumentParser('Programa que resolve o jogo do 15')
    parser.add_argument('escolha', type = str, choices = ['BFS', 'DFS', 'IDFS', 'A*-misplaced', 'A*-Manhattan', 'Greedy-misplaced', 'Greedy-Manhattan'])
    parser.add_argument('file', type=argparse.FileType('r'))
    args = parser.parse_args()

    # Ler tabuleiro de entrada de um ficheiro
    try:
        numeros = []
        f = args.file
        linhas = f.readlines()
        for linha in linhas:
            numeros += linha.split()
        estado_inicial = numeros[0:16]
        estado_final = numeros[16:33]
        f.seek(0)
    except FileNotFoundError:
        print("Ficheiro não encontrado.")
        sys.exit(1)

    numeros = []
    linhas = f.readlines()
    for linha in linhas:
        numeros += linha.split()
    b_i = numeros[0:16]
    b_f = numeros[16:32]

    # iniciar tabuleiros
    estado_inicial = Puzzle(estado_inicial)
    estado_final = Puzzle(estado_final)
    print('Configuração Inicial:')
    print(estado_inicial)
    print('Configuração Final:')
    print(estado_final)

    paridade(b_i, b_f)

    if estado_inicial == estado_final:
        print("Os estados são iguais, já está resolvido!")
        sys.exit(0)

    if args.escolha is None :
        sys.stderr.write("Forneça uma entrada válida.")
        sys.stderr.write("Escolha pelo menos um algoritmo para resolver.")
        sys.exit(1)

    if args.escolha == 'BFS':
        print("Pesquisa em Largura:")
        inicio = time.time()
        estados, movimentos, nos = bfs(estado_inicial, estado_final)
        fim = time.time()
        tempo = fim - inicio
        print("Tempo de execução: %f segundos" %tempo)
        print("Total de nós gerados e armazenados: %d" %nos)
        print('Percentagem de CPU utilizada:', psutil.cpu_percent(), '%')
        print('Percentagem de memória RAM utilizada:', psutil.virtual_memory()[2], '%')
        if movimentos:
            print("Percurso até ao estado final:")
            print(" -> ".join(movimentos))
        else:
            print("Nenhuma solução encontrada.")
            sys.exit(0)
        print()
        print("Estados até à solução:")
        for estado in estados:
            estado_puzzle = Puzzle(estado)
            print(estado_puzzle)

    if args.escolha == 'DFS':
        print("Pesquisa em Profundidade:")
        print("Indique a profundidade máxima:")
        profundidade = int(input())
        inicio = time.time()
        estados, movimentos, nos= dfs(estado_inicial, estado_final, profundidade)
        fim = time.time()
        tempo = fim - inicio
        print("Tempo de execução: %f segundos" %tempo)
        print("Total de nós gerados e armazenados: %d" %nos)
        print('Percentagem de CPU utilizada:', psutil.cpu_percent(), '%')
        print('Percentagem de memória RAM utilizada:', psutil.virtual_memory()[2], '%')
        if movimentos:
            print("Percurso até ao estado final:")
            print(" -> ".join(movimentos))
        else:
            print("Nenhuma solução encontrada até à profundidade %d. Experimente com uma profundidade maior." %profundidade)
            sys.exit(0)
        print()
        print("Estados até à solução:")
        for estado in estados:
            estado_puzzle = Puzzle(estado)
            print(estado_puzzle)

    if args.escolha == 'IDFS':
        print("Pesquisa em Profundidade Iterativa:")
        print("Indique a profundidade máxima: ")
        profundidade = int(input())
        inicio = time.time()
        estados, movimentos, nos= idfs(estado_inicial, estado_final, profundidade)
        fim = time.time()
        tempo = fim - inicio
        print("Tempo de execução: %f segundos" %tempo)
        print("Total de nós gerados e armazenados: %d" %nos)
        print('Percentagem de CPU utilizada:', psutil.cpu_percent(), '%')
        print('Percentagem de memória RAM utilizada:', psutil.virtual_memory()[2], '%')
        if movimentos:
            print("Percurso até ao estado final:")
            print(" -> ".join(movimentos))
        else:
            print("Nenhuma solução encontrada até à profundidade %d. Experimente com uma profundidade maior." %profundidade)
            sys.exit(0)
        print()
        print("Estados até à solução:")
        for estado in estados:
            estado_puzzle = Puzzle(estado)
            print(estado_puzzle)

    if args.escolha == 'A*-misplaced':
        print("Pesquisa A* Misplaced:")
        inicio = time.time()
        estados, movimentos, nos = astar(estado_inicial, estado_final, misplaced)
        fim = time.time()
        tempo = fim - inicio
        print("Tempo de execução: %f segundos" %tempo)
        print("Total de nós gerados e armazenados: %d" %nos)
        print('Percentagem de CPU utilizada:', psutil.cpu_percent(), '%')
        print('Percentagem de memória RAM utilizada:', psutil.virtual_memory()[2], '%')
        if movimentos:
            print("Percurso até ao estado final:")
            print(" -> ".join(movimentos))
        else:
            print("Nenhuma solução encontrada.")
            sys.exit(0)
        print()
        print("Estados até à solução:")
        for estado in estados:
            estado_puzzle = Puzzle(estado)
            print(estado_puzzle)

    if args.escolha == 'A*-Manhattan':
        print("Pesquisa A* Manhattan:")
        inicio = time.time()
        estados, movimentos, nos = astar(estado_inicial, estado_final, manhattan)
        fim = time.time()
        tempo = fim - inicio
        print("Tempo de execução: %f segundos" %tempo)
        print("Total de nós gerados e armazenados: %d" %nos)
        print('Percentagem de CPU utilizada:', psutil.cpu_percent(), '%')
        print('Percentagem de memória RAM utilizada:', psutil.virtual_memory()[2], '%')
        if movimentos:
            print("Percurso até ao estado final:")
            print(" -> ".join(movimentos))
        else:
            print("Nenhuma solução encontrada.")
            sys.exit(0)
        print()
        print("Estados até à solução:")
        for estado in estados:
            estado_puzzle = Puzzle(estado)
            print(estado_puzzle)

    if args.escolha == 'Greedy-misplaced':
        print("Pesquisa Greedy Misplaced:")
        inicio = time.time()
        estados, movimentos, nos = greedy(estado_inicial, estado_final, misplaced)
        fim = time.time()
        tempo = fim - inicio
        print("Tempo de execução: %f segundos" %tempo)
        print("Total de nós gerados e armazenados: %d" %nos)
        print('Percentagem de CPU utilizada:', psutil.cpu_percent(), '%')
        print('Percentagem de memória RAM utilizada:', psutil.virtual_memory()[2], '%')
        if movimentos:
            print("Percurso até ao estado final:")
            print(" -> ".join(movimentos))
        else:
            print("Nenhuma solução encontrada.")
            sys.exit(0)
        print()
        print("Estados até à solução:")
        for estado in estados:
            estado_puzzle = Puzzle(estado)
            print(estado_puzzle)

    if args.escolha == 'Greedy-Manhattan':
        print("Pesquisa Greedy Manhattan:")
        inicio = time.time()
        estados, movimentos, nos = greedy(estado_inicial, estado_final, manhattan)
        fim = time.time()
        tempo = fim - inicio
        print("Tempo de execução: %f segundos" %tempo)
        print("Total de nós gerados e armazenados: %d" %nos)
        print('Percentagem de CPU utilizada:', psutil.cpu_percent(), '%')
        print('Percentagem de memória RAM utilizada:', psutil.virtual_memory()[2], '%')
        if movimentos:
            print("Percurso até ao estado final:")
            print(" -> ".join(movimentos))
        else:
            print("Nenhuma solução encontrada.")
            sys.exit(0)
        print()
        print("Estados até à solução:")
        for estado in estados:
            estado_puzzle = Puzzle(estado)
            print(estado_puzzle)


if __name__ == '__main__':
    main()
