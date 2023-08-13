from conector import Conector
from filme import Filme
from strOrq import StrOrq
from time import sleep

class Stream(Conector):

    # Conn será um socket.socket e será a conexão com o ORQ

    def __init__(
        self,
        host:str="localhost",
        port:int=5000
    ):
        self.orq:StrOrq = None
        super().__init__(host, port)
        self.filmes: list = [
            Filme("Bacurau", 2019, "Drama", 131),
            Filme("O Auto da Compadecida", 2000, "Comédia", 104),
            Filme("O Homem que Copiava", 2003, "Comédia", 123),
            Filme("Cidade de Deus", 2002, "Drama", 130),
            Filme("O Palhaço", 2011, "Comédia", 88),
        ]


    def run(self):
        try:
            self.rodarServ()
            self.escutar()
        except (KeyboardInterrupt) as e:
            print("\n-- 1 - Servidor encerrado --\n")
        self.orq.fechar()
        self.fechar()
    
    def escutar(self):
        conn, addr = self.conn.accept()
        self.orq = StrOrq(conn=conn, addr=addr)
        print(f"\n-- Conexão estabelecida com ORQ ({self.orq.addr}) --\n")
        self.atendimento()
    
    def atendimento(self):
        while True:
            opL = self.orq.receberLista()
            op = int(opL[0])
            # print(opL[1], type(opL[1]), len(opL[1]), opL[1] == "", opL[1] == None)
            if opL[1] != "" and opL[1] != None and opL[1] != "None":
                op2 = int(opL[1])
            else:
                op2 = None
            self.selecao(op, op2)
    

    def selecao(self, op:int, op2:int=None):
        if op == 1:
            self.menu()
        
        elif op == 2:
            self.transmitirFilme(op2)

        elif op == 0:
            print("Obrigado!")
            self.orq.fechar()
            self.fechar()


    def menu(self):
        # Função que envia o menu:
        m = f"{len(self.filmes)};"
        for filme in self.filmes:
            m += f"{filme.id} - {filme.nome} ({filme.ano}) - {filme.duracao} min\n"
        self.orq.enviar(m)
        print("Menu enviado ao ORQ.")


    def transmitirFilme(self, idFilme:int):
        filme = self.buscarFilme(idFilme)
        if filme != None:
            self.orq.enviar(filme.cabecalho)
            self.enviarDados(filme)
        else:
            self.orq.enviar("0;Filme não encontrado!")
        

    def buscarFilme(self, idFilme:int):
        for filme in self.filmes:
            if filme.id == idFilme:
                return filme
        return None


    def enviarDados(self, filme:Filme):
        for dado in filme.dados:
            self.orq.enviar(f"{dado}")
            print(f"Frame {dado} / {filme.duracao}")
            sleep(0.1)
        self.orq.enviar("#")
        print(f"{filme.nome} ({filme.ano}): Enviado com sucesso!")




if __name__ == "__main__":
    stream = Stream()
    stream.run()
        

