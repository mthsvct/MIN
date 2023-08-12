from conector import Conector
from threading import Thread
import socket

class Video(Conector):

    def __init__(
        self,
        host:str="localhost",
        port:int=4000 + int(input("Digite o digito final da porta (1, 2 e 3): ")),
        conn:socket.socket=None,
        addr:tuple=None
    ) -> None:
        self.x:int = None
        self.y:int = None
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
        pass



if __name__ == "__main__":
    video = Video()
    video.run()