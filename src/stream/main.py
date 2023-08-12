from conector import Conector
from filme import Filme
from strOrq import StrOrq


class Stream(Conector):

    # Conn será um socket.socket e será a conexão com o ORQ

    def __init__(
        self,
        host:str="localhost",
        port:int=5000
    ):
        self.filmes = [
            Filme("Kill Bill", 2003, "Ação", 111),
            Filme("Barbie", 2023, "Comedia", 97),
            Filme("Bacurau", 2019, "Drama", 132),
            Filme("O Poderoso Chefão", 1972, "Drama", 175),
            Filme("Fargo", 1996, "Comedia", 98),
        ],
        self.orq:StrOrq = None
        super().__init__(host, port)
        

    def run(self):
        try:
            self.rodarServ()
            self.escutar()
        except KeyboardInterrupt:
            print("\n----- 1 - Servidor encerrado -----\n")
        self.fechar()
    
    def escutar(self):
        conn, addr = self.conn.accept()
        self.orq = StrOrq(conn=conn, addr=addr)
        print(f"\n----- Conexão estabelecida com ORQ ({self.orq.addr}) -----\n")
        self.atendimento()
    
    def atendimento(self):
        pass




if __name__ == "__main__":
    stream = Stream()
    stream.run()
        

