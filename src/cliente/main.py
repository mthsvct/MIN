import socket
from conector import Conector



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
        super().__init__(self.hostOrq, self.portOrq, conn, addr)

    def run(self):
        self.rodarCliente() # Inicia o socket e conecta com o ORQ
        self.identificar()  # Recebe o ID do cliente vindo do ORQ
        self.enviarPos()    # Envia posicao x e y para o ORQ
    
    def identificar(self):
        self.id = self.receberInt()
        print(f"----- ID do Cliente: {self.id} -----")

    def enviarPos(self):
        self.enviar(f"{self.x};{self.y}")
        print(f"----- Posição enviada: {self.x};{self.y} -----")


if __name__ == "__main__":
    c = Cliente()
    c.run()