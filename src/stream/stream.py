import socket
from time import sleep
from filme import Filme

class Stream:

    def __init__(self, host="localhost", port=4001):
        self.host = host
        self.port = port
        self.socket = None
        self.filmes = [
            Filme("Kill Bill", 120, "Acao", 2003),
            Filme("Barbie", 93, "Comedia", 2023),
            Filme("Twenty Years Later", 119, "Documentario", 1984),
            Filme("Mad Max: Fury Road", 187, "Acao", 2015),
            Filme("Misery", 107, "Suspense", 1990)]
        

    def run(self):
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            self.socket = s

            while True:
                try:
                    self.socket.bind((self.host, self.port))
                    break
                except OSError:
                    print(f"Porta {self.port} já está em uso! Aguardando 5 segundos...")
                    sleep(5)
                    
            self.socket.listen()
            print(f"Stream escutando em {self.host}:{self.port}")
            
            try:
                while True:
                    conn, addr = self.socket.accept()
                    print(f"Conectado a {addr}")
                    conn.sendall(b"Conectado ao stream") 
                    self.atendimento(conn, addr)

            except (KeyboardInterrupt, ValueError) as e: 
                print("\nEncerrando...")


    def atendimento(self, conn:socket.socket, addr:tuple):
        # 1 == Menu
        # 2;idFilme == Assistir filme
        while True:
            resOp = conn.recv(1024)
            lista = resOp.decode().split(";")
            op = int(lista[0])
            op2 = int(lista[1])
            self.sel(op, conn, addr, op2)


    def sel(self, op:int, conn:socket.socket, addr:tuple, op2:int):
        if op == 1: 
            conn.sendall(self.menu())
            print("Menu enviado ao ORQUESTRADOR.")
        elif op == 2: 
            print(f"Filme {op2} selecionado.")
            self.enviarFilme(op2, conn, addr)

    def menu(self):
        menu = f"{len(self.filmes)};"
        for i in range(len(self.filmes)): 
            menu += f"{i+1} - {self.filmes[i].nome} ({self.filmes[i].ano})\n"
        return menu.encode()
    
    def buscaFilme(self, idFilme:int) -> Filme:
        return [f for f in self.filmes if f.id == idFilme][0]
    
    def enviarFilme(self, idFilme:int, conn:socket.socket, addr:tuple):
        filme = self.buscaFilme(idFilme)
        conn.sendall(filme.cabecalho.encode())

        for i in filme.dados:
            conn.sendall(str(i).encode())
            print(f"Transmitindo filme {filme.nome} ({filme.ano}): {i}/{filme.duracao}")
            sleep(0.1)
        conn.sendall(b"#")
        print(f"Transmissão do filme {filme.nome} ({filme.ano}) ao ORQUESTRADOR FINALIZADA.")



