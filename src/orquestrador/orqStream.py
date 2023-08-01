import socket
from time import sleep
from threading import Thread
from orqFilme import OrqFilme

class OrqStream:

    def __init__(self, host="localhost", port=4000):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.menuR = None

    def run(self):
        while True:
            try:
                self.socket.connect((self.host, self.port))
                break
            except OSError:
                print("Orquestrador não pode rodar! STREAM espere. Aguardando 5 segundos...")
                sleep(5)
        dados = self.socket.recv(1024)
        print(dados.decode())
    
    def menu(self):
        # t = Thread(target=self.envia, args=("1;0")) # Solicitar o menu
        # t.start()
        # t.join()
        self.envia("1;0")
        return self.menuR

    def envia(self, dados:str):
        self.socket.sendall(dados.encode())
        print("Menu solicitado ao servidor de STREAM!")
        self.menuR = self.socket.recv(1024)


    def recebeFilme(self, idFilme:int) -> OrqFilme:
        self.socket.sendall(f"2;{idFilme}".encode())
        print("Solicitando filme ao servidor de STREAM...")

        rCabecalho = self.socket.recv(1024)
        cabecalho = rCabecalho.decode()
        print(f"Cabeçalho recebido: {cabecalho}")

        fid, nome, duracao, genero, ano = cabecalho.split(";")

        dados = []

        frame = ""

        while "#" not in frame:
            rFrame = self.socket.recv(1024)
            frame = rFrame.decode()

            if "#" not in frame:
                dados.append(int(frame))
        
        print("Recebido filme completo!", dados)

        return OrqFilme(id=int(fid), nome=nome, duracao=int(duracao), genero=genero, ano=int(ano), dados=dados)
        



