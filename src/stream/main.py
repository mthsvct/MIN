import socket
from filme import Filme

class Stream:

    def __init__(self, host="localhost", port=4001):
        self.host = host
        self.port = port
        self.socket = None
        self.filmes = [
            Filme("Kill Bill", 120, "Acao", 2003),
            Filme("Barbie", 93, "Comedia", 2023),
            Filme("Twenty Years Later", 119, "Documentario", 1984),
            Filme("Mad Max: Fury Road", 187, "Acao", 2015),
            Filme("Misery", 107, "Suspense", 1990)]
        

    def run(self):
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            self.socket = s
            self.socket.bind((self.host, self.port))
            self.socket.listen()
            print(f"Stream escutando em {self.host}:{self.port}")
            try:
                while True:
                    conn, addr = self.socket.accept()
                    print(f"Conectado a {addr}")
                    conn.sendall(b"Conectado ao stream") 
                    self.atendimento(conn, addr)

            except (KeyboardInterrupt, ValueError) as e: 
                print("\nEncerrando...")


    def atendimento(self, conn:socket.socket, addr:tuple):
        while True:
            resOp = conn.recv(1024)
            op = int(resOp.decode()) # 1 - Menu;
            self.sel(op, conn, addr)


    def sel(self, op:int, conn:socket.socket, addr:tuple):
        if op == 1: 
            conn.sendall(self.menu())
            print("Menu enviado ao ORQUESTRADOR.")
        else: 
            print("Opcao invalida!")


    def menu(self):
        menu = f"{len(self.filmes)};"
        for i in range(len(self.filmes)): 
            menu += f"{i+1} - {self.filmes[i].nome} ({self.filmes[i].ano})\n"
        return menu.encode()
    





if __name__ == "__main__":
    stream = Stream()
    stream.run()

