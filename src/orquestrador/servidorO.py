from hostPort import HostPort
import socket


class Servidor(HostPort):

    # Nesta classe possui os métodos que se comunicará com o servidor.

    def __init__(
        self,
        host:str="localhost", port:int=3000,
    ):
        super().__init__(host, port)
        self.s = None

    def run(self):
        self.conecta()
        self.s.sendall(b"0;0")
        data = self.s.recv(1024)
        print("Recebido: ", data.decode())
        self.s.close()

    def conecta(self):
        # Utilize para se conectar com o servidor.
        # Após as operações necessárias, feche a conexão com o servidor.
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((self.host, self.port)),

    def menu(self):
        self.conecta()
        self.s.sendall(b"1;0")
        menu = self.s.recv(1024)
        self.s.close()
        return menu

    def cabecalho(self, idFilme:int):
        self.conecta()
        self.s.sendall(f"2;{idFilme}".encode())
        print("Cabecalho solicitado ao servidor...")
        cabecalho = self.s.recv(1024)
        print("Cabeçalho recebido do servidor...")
        self.s.close()
        return cabecalho.decode() # Já retorna uma string
        



if __name__ == "__main__":
    servidor = Servidor("localhost", 8080)
    servidor.start()





