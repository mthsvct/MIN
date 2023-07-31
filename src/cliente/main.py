import socket


class Cliente:

    def __init__(self):
        self.orq = {"host": "localhost", "port": 2000}
        self.video = None
        self.filme = {"cabecalho": None, "dados": None}
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.x = int(input("Digite a posição x: "))
        self.y = int(input("Digite a posição y: "))

    def run(self):
        self.socket.connect((self.orq["host"], self.orq["port"]))
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

            if op == 0: break




if __name__ == "__main__":
    cliente = Cliente()
    cliente.run()
