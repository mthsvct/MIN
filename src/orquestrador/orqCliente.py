import socket
from conector import Conector


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
    
    def inicializacao(self):
        self.enviar(f"{self.id}") # Enviar ID para o cliente
        self.receberPos()          # Recebe a posição do cliente

    def receberPos(self):
        pos = self.receberLista()
        self.x, self.y = int(pos[0]), int(pos[1])
        print(f"----- Posição do cliente {self.id}: {self.x};{self.y} -----")

    def enviarMenu(self, menu:str):
        # Caso seja necessário realizar alguma alteração, farei aqui.
        return self.enviar(msg=menu)
