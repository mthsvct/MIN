import socket
from conector import Conector
from vidFilme import VidFilme



class VidOrq(Conector):


    def __init__(
        self, 
        host: str = None, 
        port: int = None, 
        conn: socket = None, 
        addr: tuple = None
    ) -> None:
        super().__init__(host, port, conn, addr)

    
    def receberFilme(self):
        filme = self.receberCabecalho()
        filme.dados = self.recebeDados(duracao=filme.duracao)
        return filme

    def receberCabecalho(self):
        cabecalho = self.receberLista()
        # idFilme, nome, ano, genero, duracao = cabecalho
        idFilme = int(cabecalho[0])
        nome = cabecalho[1]
        ano = int(cabecalho[2])
        genero = cabecalho[3]
        duracao = int(cabecalho[4])
        return VidFilme(idFilme, nome, ano, genero, duracao)
        
    def recebeDados(self, duracao:int):
        dados = []
        frame = ""
        while "#" not in frame:
            frame = self.receber()
            if "#" not in frame:
                dados.append(int(frame))
            print(f"Frame recebido: {frame} / {duracao}")
        return dados