import socket
from threading import Thread
from conector import Conector
from orqStream import OrqStream
from orqVideo import OrqVideo
from orqCliente import OrqCliente
from math import sqrt

class Orq(Conector):

    def __init__(
        self,
        host:str="localhost",
        port:int=3000,
        hostStr:str="localhost",
        portStr:int=5000,
        hostVid:str="localhost",
        portVid:int=4000,
    ):
        self.hostStr = hostStr
        self.portStr = portStr
        self.hostVid = hostVid
        self.portVid = portVid
        self.stream:OrqStream = OrqStream(hostStr, portStr)
        self.videos:list = None
        self.clientes:list = []
        super().__init__(host, port)


    def run(self):
        try:
            self.conectaStream()
            self.conectaVideos()
            self.iniciarOrq()
            
        except (KeyboardInterrupt, BrokenPipeError) as e:
            print("\n----- 1 - Servidor encerrado -----\n")
            self.fechar()
            _ = [ v.fechar() for v in self.videos ]


    def conectaStream(self):
        self.stream = OrqStream(self.hostStr, self.portStr)
        self.stream.run()
        

    def conectaVideos(self):
        posicoes = [(2, 6)]
        self.videos = [OrqVideo(self.hostVid, self.portVid + i, x=p[0], y=p[1]) for i, p in enumerate(posicoes, 1) ]
        for v in self.videos: v.run()
        

    def iniciarOrq(self):
        self.rodarServ()
        self.escutar()


    def escutar(self):
        while True:
            conn, addr = self.conn.accept()
            print(f"\n----- Conexão estabelecida com cliente ({addr}) -----\n")
            cliente = OrqCliente(conn=conn, addr=addr)
            self.clientes.append(cliente)
            nova = Thread(target=self.atendimento, args=(cliente,))
            nova.start()
    

    def atendimento(self, cliente:OrqCliente):
        try:
            print(f"\nAtendimento iniciado... ao cliente {cliente.id}\n")
            cliente.inicializacao() # Função que fará etapas iniciais do cliente
            self.calcularDistancias(cliente) # Calcula as distâncias do cliente para os vídeos
            self.gerExibicaoFilmes(cliente) # Gerencia a exibição dos filmes para o cliente
        except (KeyboardInterrupt, ConnectionResetError) as e:
            print("Conexão com cliente encerrado!")
            cliente.fechar()

    def calcularDistancias(self, cliente:OrqCliente):
        cliente.distancias = [ (v.id, self.distancia(cliente, v)) for v in self.videos ]
        cliente.distancias.sort(key=lambda x: x[1])


    def distancia(self, cliente:OrqCliente, video:OrqVideo):
        x1, y1 = cliente.x, cliente.y
        x2, y2 = video.x, video.y
        distancia = sqrt((x2 - x1)**2 + (y2 - y1)**2)
        return round(distancia, 2)


    def gerExibicaoFilmes(self,cliente:OrqCliente):
        op = -1
        while op != 0:
            op = self.menu(cliente) # Requisita, recebe o menu do STREAM e depois envia ao CLIENTE
            self.selecao(cliente, op) # Recebe a seleção do cliente e segue as funções de acordo com a opção


    def menu(self, cliente:OrqCliente):
        menu = self.stream.receberMenu()
        cliente.enviarMenu(menu)
        op = cliente.receberInt()
        print(f"----- Opção recebida: {op} - {type(op)} -----")
        

    def selecao(self, cliente:OrqCliente, op:int):
        if op == 0:
            # Encerrar conexão com cliente
            cliente.fechar()
        else:
            pass


        
if __name__ == "__main__":
    orq = Orq()
    orq.run()



