import socket

from conector import Conector
from cliFilme import CliFilme


class CliVideo(Conector):


    def __init__(
        self, 
        host: str = None, 
        port: int = None, 
        conn: socket.socket = None, 
        addr: tuple = None,
        distancia: float = None,
    ) -> None:
        self.distancia = distancia
        super().__init__(host, port, conn, addr)


    def run(self, idOrq:int=0):
        self.rodarCliente()           # Se conecta com o servidor de vídeo
        self.enviar(f"2;{idOrq};{self.distancia};")    # Envia sinal de que é um cliente e o id do orquestrador
        
    
    def exibirFilme(self):
        filme = self.receberFilme() # Recebe o filme do servidor de vídeo
        self.terminar()     # Fecha a conexão com o servidor de vídeo
        return filme

    def receberFilme(self):
        filme = self.receberCabecalho()
        filme.dados = self.recebeDados(duracao=filme.duracao)
        return filme
    
    def terminar(self):
        # Fecha a conexão com o vídeo e faz qualquer outra coisa que precisar.
        self.fechar()

    def receberCabecalho(self) -> CliFilme:
        # Recebe o cabeçalho do filme
        cabecalho = self.receberLista()

        print(cabecalho)

        idFilme = int(cabecalho[0])
        nome = cabecalho[1]
        ano = int(cabecalho[2])
        genero = cabecalho[3]
        duracao = int(cabecalho[4])
        return CliFilme(idFilme, nome, ano, genero, duracao)

    def recebeDados(self, duracao:int):
        # Recebe os dados do filme
        dados = []
        frame = ""
        while "#" not in frame:
            frame = self.receber()
            if "#" not in frame:
                dados.append(int(frame))
            print(f"Frame recebido do VIDEO: {frame} / {duracao}")
        return dados
