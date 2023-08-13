import socket
from math import sqrt
from conector import Conector
from orqVideo import OrqVideo

class OrqCliente(Conector):

    id:int = 1

    def __init__(
        self, 
        conn: socket.socket = None, 
        addr: tuple = None,
        host: str = None, 
        port: int = None, 
        x:int=None,
        y:int=None
    ) -> None:
        self.id = OrqCliente.id
        self.x = x
        self.y = y
        self.distancias = [] # distancias = [ (id_video, distancia), ... ]
        super().__init__(host, port, conn, addr)
        OrqCliente.id += 1
    
    def inicializacao(self, videos:list):
        self.enviar(f"{self.id}") # Enviar ID para o cliente
        self.receberPos()          # Recebe a posição do cliente
        self.calcularDistancias(videos) # Calcula as distâncias entre o cliente e os vídeos

    def receberPos(self):
        pos = self.receberLista()
        self.x, self.y = int(pos[0]), int(pos[1])
        print(f"----- Posição do cliente {self.id}: {self.x};{self.y} -----")


    def enviarMenu(self, menu:str):
        # Caso seja necessário realizar alguma alteração, farei aqui.
        return self.enviar(msg=menu)


    def calcularDistancias(self, videos:list):
        self.distancias = [ (v, self.distancia(v)) for v in videos ]
        self.distancias.sort(key=lambda x: x[1])


    def distancia(self, video:OrqVideo):
        x1, y1 = self.x, self.y
        x2, y2 = video.x, video.y
        distancia = sqrt((x2 - x1)**2 + (y2 - y1)**2)
        return round(distancia, 2)


    def buscaDistancia(self, vId:int):
        retorno = None
        for distancia in self.distancias:
            if distancia[0].id == vId:
                retorno = distancia[1]
                break
        return retorno