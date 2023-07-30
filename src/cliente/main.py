import socket


def lerMenu(qnt, op:int=-1):    
    while op < 0 or op > qnt: 
        op = int(input("Digite a opção desejada: "))
        if op < 0 or op > qnt: print("Opção inválida.")
    return op

def showMenu(menuR):
    qnt, M = menuR.decode().split(";")
    print("Menu: \n", M)
    return lerMenu(int(qnt))

def menu(s):
    # Função que recebe o menu do orquestrador 
    # Apresenta o menu para o usuário
    # Recebe a opção escolhida pelo usuário
    menuR = None
    while menuR is None or menuR == b"": 
        menuR = s.recv(1024)
    op = showMenu(menuR)
    s.sendall(str(op).encode())
    return op



host = "localhost"
port = 2000 # Porta da comunicação do orquestrador.

# Criando o socket.
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))

x = int(input("Digite a posicao X: "))
y = int(input("Digite a posicao Y: "))

sinal = f"1;{x};{y}"

# Enviando o tipo do dispositivo.
s.sendall(sinal.encode())
op = menu(s)
cabecalho = s.recv(1024)


# if cabecalho is not None:
#     _, nome, duracao, ano = cabecalho.decode().split(";")
#     print(f"Recebendo filme: {nome} ({ano}) - {duracao} min ")
# else:
#     print("Filme não encontrado.")

s.close()



