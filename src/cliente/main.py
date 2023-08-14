import socket
from time import sleep

from conector import Conector
from cliVideo import CliVideo
from cliFilme import CliFilme

class Cliente(Conector):


    def __init__(
        self, 
        host: str = None, 
        port: int = None, 
        conn: socket.socket = None, 
        addr: tuple = None
    ) -> None:
        self.id:int = None
        self.x:int = int(input("Digite a posição x: "))
        self.y:int = int(input("Digite a posição y: "))
        self.hostOrq:str = "localhost"
        self.portOrq:int = 3000
        self.video:CliVideo = None
        self.filme:CliFilme = None
        super().__init__(self.hostOrq, self.portOrq, conn, addr)


    def run(self):
        self.rodarCliente() # Inicia o socket e conecta com o ORQ
        self.identificar()  # Recebe o ID do cliente vindo do ORQ
        self.enviarPos()    # Envia posicao x e y para o ORQ
        self.atendimento()  # Recebe o IP e PORTA do servidor de jogo
    

    def identificar(self):
        self.id = self.receberInt()
        print(f"----- ID do Cliente: {self.id} -----")


    def enviarPos(self):
        self.enviar(f"{self.x};{self.y}")
        print(f"----- Posição enviada: {self.x};{self.y} -----")
    

    def atendimento(self):
        op = -1
        while op != 0:
            op = self.menu() # Solicita o Menu de filmes do Orquestrador
            if op != 0: 
                self.selecao() # Se opção for diferente de 0, solicita a seleção de um filme

    def menu(self):
        qnt = self.apresentaMenu()
        op = -1
        while op < 0 or op > qnt:
            op = int(input("Digite a opção: "))
        self.enviar(f"{op}")
        print("\n\n")
        return op

    def apresentaMenu(self):
        l = self.receberLista()
        qnt, menu= int(l[0]), l[1]
        print(f"\n\n----- Menu de Filmes -----")
        print(menu, end="")
        print("0 - Sair")
        return qnt

    def selecao(self):
        self.iniciaVideo()

    def iniciaVideo(self):
        endLista = self.receberLista()
        host, port, distancia = endLista[0], int(endLista[1]), float(endLista[2])
        print("Distancia: ", distancia)
        self.video = CliVideo(host=host, port=port, distancia=distancia)
        self.video.run(idOrq=self.id)
        self.filme = self.video.exibirFilme()
        print("----- Filme recebido e assistido! -----")
        print(self.filme)
        print("\n" * 2)





if __name__ == "__main__":
    c = Cliente()
    c.run()