import socket

from conector import Conector
from vidFilme import VidFilme
from time import sleep

class VidCliente(Conector):


    def __init__(
        self, 
        host: str = None, 
        port: int = None, 
        conn: socket.socket = None, 
        addr: tuple = None,
        idOrq: int = None,
        distancia: float = None,
    ) -> None:
        self.id = idOrq
        self.distancia = distancia
        self.latencia = distancia * 0.1
        super().__init__(host, port, conn, addr)


    def __str__(self) -> str:
        return f"Cliente {self.id} em {self.addr} - Distância: {self.distancia}"

    def transmitirFilme(self, filme:VidFilme):
        if filme != None:
            print(f"\n\nTransmissão do filme {filme}:\npara o cliente {self}\nCom a latencia = {self.latencia}\n\n")
            self.enviar(filme.cabecalho)
            self.enviarDados(dados=filme.dados, duracao=filme.duracao)
            print(f"{filme.nome} ({filme.ano}): Enviado ao VIDEO com sucesso!")
        else:
            self.enviar("0;Filme não encontrado!")

    def enviarDados(self, dados:list, duracao:int=None):
        for dado in dados:
            self.enviar(f"{dado}")
            print(f"Frame ENVIADO ao CLIENTE: {dado} / {duracao}")
            sleep(self.latencia)
        self.enviar("#")
        