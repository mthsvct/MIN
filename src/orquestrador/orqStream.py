import socket
from threading import Thread


class OrqStream:

    def __init__(self, host="localhost", port=4000):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.menuR = None

    def run(self):
        self.socket.connect((self.host, self.port))
        dados = self.socket.recv(1024)
        print(dados.decode())
    
    def menu(self):
        t = Thread(target=self.envia, args=("1"))
        t.start()
        t.join()
        return self.menuR

    def envia(self, dados:str):
        self.socket.sendall(dados.encode())
        print("Menu solicitado ao servidor de STREAM!")
        self.menuR = self.socket.recv(1024)



