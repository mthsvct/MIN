from conector import Conector
from vidOrq import VidOrq
from threading import Thread
import socket

class Video(Conector):

    def __init__(
        self,
        host:str="localhost",
        port:int=4000 + int(input("Digite o digito final da porta (1, 2 e 3): ")),
        conn:socket.socket=None,
        addr:tuple=None,
        status:int=0, # 0 - Disponível, 1 - Ocupado
    ) -> None:
        self.x:int = None
        self.y:int = None
        self.orq:VidOrq = None
        self.status:int = status
        self.limite:int = int(input("Digite o limite de clientes por vídeo: "))
        super().__init__(host, port, conn, addr)


    def run(self):
        try:
            self.rodarServ()
            self.escutar()
        except KeyboardInterrupt:
            print("\n----- 1 - Servidor encerrado -----\n")
        self.fechar()


    def escutar(self):
        while True:
            conn, addr = self.conn.accept()
            print(f"\n----- Conexão estabelecida com ORQ ({self.addr}) -----\n")
            nova = Thread(target=self.atendimento, args=(conn, addr,))
            nova.start()

    def atendimento(self, conn:socket.socket, addr:tuple):
        print(f"Atendimento do video.")

        # Primeiro recebe um sinal informando que tipo de cliente é
        # 1 - Orquestrador
        # 2 - Cliente

        tipo = conn.recv(1024).decode()
        
        if tipo == "1":
            self.orq = VidOrq(conn=conn, addr=addr)
            self.orq.enviar(f"{self.limite}")
        elif tipo == "2":
            pass

    



if __name__ == "__main__":
    video = Video()
    video.run()