import socket
from time import sleep

class Conector:

    def __init__(
        self, 
        host:str=None,
        port:int=None,
        conn:socket.socket=None,
        addr:tuple=None
    ) -> None:
        self.host = host
        self.port = port
        self.conn = conn
        self.addr = addr
    
    
    def fechar(self):
        if self.conn != None:
            self.conn.close()
            print("\n-- Conexão fechada --\n")
        else:
            print("\n-- Conexão não estabelecida --\n")
    
    def enviar(self, msg:str):
        if self.conn != None: 
            self.conn.send(msg.encode())
            # print(f"\n----- Enviado: {msg} para {self.addr} -----\n")
        else:
            print("\n-- Conexão não estabelecida --\n")

    def receber(self):
        msg = None
        if self.conn != None:
            msg = self.conn.recv(1024).decode()
            # print(f"\n-- Recebido: {msg} de {self.addr} --\n")
        else:
            print("\n-- Conexão não estabelecida --\n")
        return msg
    
    def receberInt(self):
        msg = self.receber()
        return int(msg) if msg != None else None
    
    def receberLista(self):
        msg = self.receber()
        return msg.split(";") if msg != None else None
    
    

    # ------------------- CONN será um SERVIDOR ------------------- #
    
    def rodarServ(self):
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.vincular()
        self.conn.listen()

    def vincular(self):
        while True:
            try:
                self.conn.bind((self.host, self.port))
                print(f"\n-- Servidor rodando em {self.host}:{self.port} --\n")
                break
            except OSError:
                print("\n-- Porta em uso, tentando novamente em 3 segundos -- \n")
                sleep(3)

    # ------------------- CONN será um CLIENTE ------------------- #

    def rodarCliente(self): 
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conectar()
        
    def conectar(self):
        while True:
            try:
                self.conn.connect((self.host, self.port))
                print(f"\n-- Conectado a {self.host}:{self.port} --\n")
                break
            except OSError:
                print("\n-- Servidor não encontrado, tentando novamente em 3 segundos -- \n")
                sleep(3)

