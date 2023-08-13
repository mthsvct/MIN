import socket
from conector import Conector


class OrqVideo(Conector):

    id:int = 1

    def __init__(
        self, 
        host: str = None, 
        port: int = None, 
        conn: socket.socket = None, 
        addr: tuple = None,
        x:int=None,
        y:int=None,
        status:int=0, # 0 - Disponível, 1 - Ocupado
    ) -> None:
        self.id = OrqVideo.id
        self.x = x
        self.y = y
        self.status = status
        self.filme = None
        self.limite:int = 3,
        self.clientes:list = []
        super().__init__(host, port, conn, addr)
        OrqVideo.id += 1

    def run(self):
        self.rodarCliente()
        self.enviar("1")
        self.limite = self.receberInt()
        print(f"\n -- Limite enviado pelo video: {self.limite} -- \n")

    def haVaga(self):
        # Retorna
            # 1: True - Se há vaga
            # 2: Quantas vagas ainda há
        return len(self.clientes) < self.limite, self.limite - len(self.clientes)