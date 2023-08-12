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
        y:int=None
    ) -> None:
        self.id = OrqVideo.id
        self.x = x
        self.y = y
        super().__init__(host, port, conn, addr)
        OrqVideo.id += 1

    def run(self):
        self.rodarCliente()