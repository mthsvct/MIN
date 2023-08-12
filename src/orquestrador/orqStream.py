import socket
from conector import Conector


class OrqStream(Conector):

    def __init__(
        self, 
        host:str=None, 
        port:int=None, 
        conn:socket.socket=None, 
        addr:tuple=None
    ) -> None:
        super().__init__(host, port, conn, addr)

    
    def run(self):
        self.rodarCliente()