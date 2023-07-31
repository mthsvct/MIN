import socket


class OrqCliente:

    id = 1

    def __init__(self, host="localhost", port=2000, x=0, y=0, conn=None, addr=None):
        self.host = host
        self.port = port
        self.socket = None
        self.x = x
        self.y = y
        self.id = OrqCliente.id
        self.addr = addr
        self.conn:socket.socket = conn
        OrqCliente.id += 1

    def run(self, orq):
        dados = self.conn.recv(1024)
        print(f"Dados recebidos do cliente {self.id}: {dados.decode()}")
        lista = dados.decode().split(";")
        self.x, self.y = int(lista[0]), int(lista[1])
        orq.calcularDistancias(self)
        print(f"Cliente possui as seguintes coordenadas: ({self.x}, {self.y})")
        self.conn.sendall(b"Dados recebidos! Obrigado!")


