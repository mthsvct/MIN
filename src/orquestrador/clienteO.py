from hostPort import HostPort
from posicoes import Posicoes
import socket
from time import sleep


class Cliente(HostPort, Posicoes):

    total = 0

    def __init__(
        self, 
        x:int, y:int,
        host:str="localhost", port:int=2000, 
        idFilme:int=0,
        thr:int=0,
        status:str="espera",
        conn:socket=None,
        addr:tuple=None,
    ):
        self.id = Cliente.total
        Cliente.total += 1
        self.thr = thr
        self.idFilme = idFilme
        self.status = status
        self.conn = conn
        self.addr = addr
        HostPort.__init__(self, host=host, port=port)
        Posicoes.__init__(self, x, y)

    def __str__(self): return f"Cliente:{self.id}\nAddr:{self.addr}\nPosicao:{self.x},{self.y}"

    def run(self, menu:str='', orq=None):
        print("Enviando menu para o cliente...")
        self.conn.sendall(menu)
        print("Menu enviado para o cliente...")
        op = self.conn.recv(1024)
        print("Opção recebido: ", op.decode())
        self.selectFilme(int(op.decode()), orq)
    
    def selectFilme(self, op, orq):
        if op > 0:
            self.idFilme = op - 1
            self.status = "espera"
            # orq.solicitaFilme(self, self.idFilme)
        
if __name__ == "__main__":
    cliente = Cliente(
        host="localhost", 
        port=8080,
        x=0, y=0, 
        idFilme=0
    )
    cliente.start()


