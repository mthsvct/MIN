import socket
from time import sleep

class Cliente:

    def __init__(self):
        self.orq = {"host": "localhost", "port": 2000}
        self.video = None
        self.filme = {"cabecalho": None, "dados": None}
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.x = int(input("Digite a posição x: "))
        self.y = int(input("Digite a posição y: "))

        self.video = None

    def run(self):
        
        while True:
            try:
                self.socket.connect((self.orq["host"], self.orq["port"]))
                break
            except ConnectionRefusedError:
                print("Servidor de vídeos não está ativo! Aguardando 5 segundos...")
                sleep(5)
        
        self.socket.sendall(f"{self.x};{self.y}".encode()) # Envia as posições do cliente
        dados = self.socket.recv(1024)
        print(dados.decode())
        self.servico()

    def menu(self, menu:str, qnt:int):
        print(menu)
        print("0 - Sair")
        op = -1
        while op < 0 or op > qnt:
            op = int(input("\nDigite a opção desejada: "))
            print("Opção inválida!\n" if (op < 0 or op > qnt) else "", end="") 
        return op    

    def servico(self):
        while True:
            rMenu = self.socket.recv(1024)
            lista = rMenu.decode().split(";")
            op = self.menu(lista[1], int(lista[0]))
            self.socket.sendall(str(op).encode())
            self.receberVideo()

            if op == 0: break

    def receberVideo(self):
        dados = self.socket.recv(1024)
        print(dados.decode())
        lista = dados.decode().split(";")
        distancia = float(lista[2])
        idOrq = int(lista[3])
        self.video = {
            "host": lista[0],
            "port": int(lista[1]),
            "distancia": distancia
        }

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.video["host"], self.video["port"]))
            s.sendall(f"2;{self.video['distancia']}".encode())
            self.receberFilme(s)


    def receberFilme(self, s:socket.socket):
        dados = s.recv(1024)
        print(dados.decode())
        lista = dados.decode().split(";")
        self.filme["cabecalho"] = {
            "id": int(lista[0]),
            "nome": lista[1],
            "duracao": int(lista[2]),
            "genero": lista[3],
            "ano": int(lista[4]),
        }

        d = []
        f = ""

        while "#" not in f:
            f = s.recv(1024).decode()
            if "#" not in f:
                d.append(int(f))
                print(f"Rebendo dados do filme {self.filme['cabecalho']['nome']} ({self.filme['cabecalho']['ano']}): {f}/{self.filme['cabecalho']['duracao']}.")





if __name__ == "__main__":
    cliente = Cliente()
    cliente.run()
