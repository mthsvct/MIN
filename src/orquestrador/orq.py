import socket
from math import sqrt

from threading import Thread
from orqVideo import OrqVideo
from orqCliente import OrqCliente
from orqStream import OrqStream as Stm

class Orquestrador:

    def __init__(self, host="localhost", port=2000, hostStream="localhost", portStream=4001, hostVideos="localhost", portVideos=3000):
        self.host = host
        self.port = port
        self.socket = None
        self.hostStream = hostStream
        self.portStream = portStream
        self.stream = None
        self.hostVideos = hostVideos
        self.portVideos = portVideos
        self.thrStream = None
        self.videos = []
        self.thrsVideos = [] # Threads de conexões de vídeos
        self.thrs = []
        self.distancias = []
        self.clientes = []



    def run(self):
        self.conectaStream()
        self.conectaVideos()
        self.conectaClientes()
    
    def conectaStream(self):
        self.stream = Stm(self.hostStream, self.portStream)
        self.thrStream = Thread(target=self.stream.run)
        self.thrStream.start()
    
    def conectaVideos(self):
        pos = [(2, 6)]
        self.videos = [ OrqVideo(self.host, self.portVideos + i, x=pos[i-1][0], y=pos[i-1][1]) for i in range(1,2) ]
        for i in self.videos: print(i.port)
        self.thrsVideos = [ Thread(target=video.run) for video in self.videos ]
        for thr in self.thrsVideos: thr.start()

    def conectaClientes(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen()
            print(f"Orquestrador escutando em {self.host}:{self.port}")

            try:
                while True:
                    conn, addr = s.accept()
                    novo = OrqCliente(conn=conn, addr=addr)
                    self.thrs.append(Thread(target=self.runCliente, args=(novo,)))
                    self.thrs[-1].start()

            except:
                print("\nEncerrando...")
                for thr in self.thrs: thr.join()
                for thr in self.thrsVideos: thr.join()
                self.thrStream.join()

    def runCliente(self, novo:OrqCliente):

        print(f"Cliente com id {novo.id} e endereco {novo.addr} conectado!")

        dados = novo.conn.recv(1024)
        print(f"Dados recebidos do cliente {novo.id}: {dados.decode()}")

        lista = dados.decode().split(";")
        novo.x, novo.y = int(lista[0]), int(lista[1])
        self.calcularDistancias(novo)

        print(f"Cliente possui as seguintes coordenadas: ({novo.x}, {novo.y})")
        self.clientes.append(novo)

        novo.conn.sendall(b"Dados recebidos! Obrigado!")

        self.transmitirFilmes(novo)


    def calcularDistancias(self, cliente:OrqCliente):

        for video in self.videos:
            x1, y1 = cliente.x, cliente.y
            x2, y2 = video.x, video.y
            distancia = sqrt((x2 - x1)**2 + (y2 - y1)**2)
            self.distancias.append((cliente.id, video.id, distancia))


    def transmitirFilmes(self, cliente:OrqCliente):
        op = -1
        while op != 0:
            cliente.conn.sendall(self.stream.menu())
            print("Menu enviado ao CLIENTE.")

            resOp = cliente.conn.recv(1024) # Recebe a opção escolhida pelo cliente. IdFilme
            op = int(resOp.decode())
            print(f"Opção escolhida pelo CLIENTE: {op}")


        print(f"Encerrando conexão com cliente de endereco {cliente.id} {cliente.addr}")
