import socket
from time import sleep
from conector import Conector
from orqFilme import OrqFilme
from threading import Thread

class OrqStream(Conector):

    def __init__(
        self, 
        host:str=None, 
        port:int=None, 
        conn:socket.socket=None, 
        addr:tuple=None
    ) -> None:
        self.blocked:bool = False # True - Bloqueado, False - Desbloqueado.
        # Blocked serve para bloquear o envio de filmes para os clientes.
        super().__init__(host, port, conn, addr)

    def run(self):
        self.rodarCliente()
    
    def receberMenu(self):
        # Caso precise fazer alguma alteração farei aqui.
        self.enviar(f"{1};{0}")
        return self.receber()

    def recebeFilme(self, idFilme:int) -> OrqFilme:

        while self.blocked == True:
            print("O servidor de STREAM, está ocupado. Aguardando 1 segundo.\n")
            sleep(1)

        self.blocked = True
        self.enviar(f"{2};{idFilme}")
        filme = self.recebeCabecalho()
        filme.dados = self.recebeDados(filme.duracao)
        self.blocked = False
        return filme

    def recebeCabecalho(self):
        cabecalho = self.receber()
        lista = cabecalho.split(";")
        idFilme = int(lista[0])
        nome = lista[1]
        ano = int(lista[2])
        genero = lista[3]
        duracao = int(lista[4])
        filme = OrqFilme(idFilme, nome, ano, genero, duracao)
        return filme
    
    def recebeDados(self, duracao:int):
        dados = []
        frame = ""
        while "#" not in frame:
            frame = self.receber()
            if "#" not in frame:
                dados.append(int(frame))
            print(f"Frame recebido do STREAM: {frame} / {duracao}")
        return dados