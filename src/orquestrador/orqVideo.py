import socket
from time import sleep
from conector import Conector
from orqFilme import OrqFilme

class OrqVideo(Conector):

    id:int = 1

    def __init__(
        self, 
        host: str = None, 
        port: int = None, 
        conn: socket.socket = None, 
        addr: tuple = None,
        x:int=None,
        y:int=None,
        status:int=0, # 0 - Disponível, 1 - Ocupado
    ) -> None:
        self.id = OrqVideo.id
        self.x = x
        self.y = y
        self.status = status
        self.filme:OrqFilme = None
        self.limite:int = 3,
        self.clientes:list = []
        self.transmitindo:bool = False
        self.recebendo:bool = False
        super().__init__(host, port, conn, addr)
        OrqVideo.id += 1

    def __str__(self) -> str:
        return f"id: {self.id}, \nx: {self.x}, y: {self.y}, \nstatus: {self.status}, \nlimite: {self.limite}, \nclientes: {len(self.clientes)}, \nfilme: {self.filme}\n"

    def __repr__(self) -> str:
        return f"OrqVideo(id={self.id}, x={self.x}, y={self.y}, status={self.status}, limite={self.limite}, clientes={len(self.clientes)}, filme={self.filme})\n\n"

    def infos(self) -> str:
        return f"id: {self.id}\nx: {self.x}, y: {self.y}\nHa vaga: {self.haVaga()}\nStatus: {self.statusStr()}\nLimite: {self.limite}\nClientes: {len(self.clientes)}\nFilme: {self.filme}"

    def run(self):
        self.rodarCliente()
        self.enviar("1;0")
        self.limite = self.receberInt()

    def haVaga(self):
        # Retorna
            # 1: True - Se há vaga
            # 2: Quantas vagas ainda há
        return len(self.clientes) < self.limite, self.limite - len(self.clientes)

    def statusStr(self):
        return "Disponível" if self.status == 0 else "Ocupado"    

    def transmitirFilme(self, filme:OrqFilme):

        if filme != None:
            self.recebendo = True
            self.enviar("1;0;")
            self.enviar(filme.cabecalho)
            self.enviarDados(dados=filme.dados, duracao=filme.duracao)
            self.recebendo = False
            print(f"{filme.nome} ({filme.ano}): Enviado ao VIDEO com sucesso!")
        else:
            self.enviar("0;Filme não encontrado!")
        
    
    def enviarDados(self, dados:list, duracao:int=None):
        for dado in dados:
            self.enviar(f"{dado}")
            print(f"Frame ENVIADO ao VIDEO: {dado} / {duracao}")
            sleep(0.1)
        self.enviar("#")