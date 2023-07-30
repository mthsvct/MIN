import socket
from time import sleep


host = "localhost"
port = 2000 # Porta da comunicação do orquestrador.
clientes = []



# Enviando o tipo do dispositivo.
x = int(input("Digite a posicao X: "))
y = int(input("Digite a posicao Y: "))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port)) # Conectando ao orquestrador.
    s.sendall(f"2;{x};{y}".encode()) # Mandando um sinal para o orquestrador, informando que é um vídeo.
    res = s.recv(1024)
    print("Resposta: ", res.decode())

    while True:
        sleep(1)
        cabecalho = s.recv(1024)
        if cabecalho is not None and cabecalho != b"":
            break
    
    print("Cabecalho: ", cabecalho.decode())

