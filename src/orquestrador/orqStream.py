import socket
from conector import Conector
from threading import Thread

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
    
    
    def receberMenu(self):
        # Caso precise fazer alguma alteração farei aqui.
        self.enviar(f"{1};{0}")
        return self.receber()
