import socket
from time import sleep



host = "localhost"
port = 2000 # Porta da comunicação do orquestrador.
clientes = []




# Enviando o tipo do dispositivo.
x = int(input("Digite a posicao X: "))
y = int(input("Digite a posicao Y: "))

# Criando o socket.
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port)) # Conectando ao orquestrador.


sinal = f"2;{x};{y}"
s.sendall(sinal.encode())

res = s.recv(1024)
print("Resposta: ", res.decode())

while True:
    cabecalho = s.recv(1024)
    print("Cabecalho: ", cabecalho.decode())

filme = None


