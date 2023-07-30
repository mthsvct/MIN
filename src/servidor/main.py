from filme import Filme
import socket


filmes = [
    Filme("Kill Bill", 111, 2003, "Ação"),
    Filme("The Graduate", 106, 1967, "Drama"),
    Filme("Barbie", 89, 2023, "Comedia"),
    Filme("Sunset Boulevard", 100, 1950, "Drama"),
    Filme("Bacurau", 131, 2019, "Ação"),
]

def menu():
    menu = f"{len(filmes)};\n"
    for i, filme in enumerate(filmes): 
        menu += f"{i+1} - {filme.nome} ({filme.ano}) - {filme.duracao}min\n"
    menu += "0 - Sair\n"
    return menu.encode()

def selecao(op:str, s:socket.socket, conn:socket.socket, addr:tuple):
    opI, opF = op.split(";")
    escolha, idFilme = int(opI), int(opF)
    if escolha == 0:
        conn.sendall(b"Conectado ao servidor com sucesso!")
    elif escolha == 1:
        # Enviar menu de filmes para o endereço conectado.
        conn.sendall(menu())
    elif escolha == 2:
        # Enviar cabeçalho de filme para o endereço conectado.
        cabecalho = f"{idFilme};{filmes[idFilme].nome};{filmes[idFilme].duracao};{filmes[idFilme].ano}"
        conn.sendall(cabecalho.encode())


host = "localhost"
port = 3000 # Porta da comunicação do orquestrador.



# 0; - Envia mensagem informando que está conectado com o servidor.
# 1; - Envie menu de filmes para o endereço conectado.
# 2;x; - Enviar cabecalho de filme para o endereço conectado.
#   2  - Opção que informa que se quer selecionar um filme;
#   x  - Número do filme escolhido.


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

    # s é um socket.

    s.bind((host, port))
    s.listen()

    print("Servidor aguardando conexões...")

    while True:

        conn, addr = s.accept()
        print("Conectado por: ", addr)

        while True:
            op = conn.recv(1024)
            if op is not None or op != b"": break

        print("Recebido: ", op.decode())

        selecao(op.decode(), s, conn, addr)
        conn.close()
        