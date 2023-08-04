import socket
from vidFilme import VidFilme
from time import sleep

class VidCliente:

    def __init__(self, id:int, host:str, port:int, distancia:float, conn:socket.socket=None, addr:tuple=None):
        self.id = id
        self.host = host
        self.port = port
        self.distancia = distancia
        self.conn = conn
        self.addr = addr
        self.latencia = (distancia * 0.1)

    def enviar(self, filme:VidFilme):

        print(f"Enviando filme {filme} para o cliente {self.id}...")
        self.conn.sendall(filme.cabecalho.encode())
        print(f"Cabecalho enviado para o CLIENTE {self.id}: {filme} com latencia {self.latencia}.\n")

        for dado in filme.dados:
            self.conn.sendall(f"{dado}".encode())
            print(f"Dado do filme {filme} enviado para o CLIENTE {self.id}: {dado}/{filme.duracao}.")
            sleep(self.latencia)

        self.conn.sendall("#".encode())
        print(f"Filme {filme} enviado para o CLIENTE {self.id}!\n")
