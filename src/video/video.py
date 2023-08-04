import socket
from time import sleep
from vidFilme import VidFilme
from vidCliente import VidCliente
from threading import Thread

class Video:

    id = 1

    def __init__(self, host="localhost", port=3001):
        self.id = Video.id
        self.host = host
        self.port = port
        self.socket = None
        self.x:int = None
        self.y:int = None
        self.thrs = []
        self.filme:VidFilme = None
        self.limite:int = int(input("Digite o limite de clientes deste video: "))
        Video.id += 1
        self.orq = None
        self.clientes = []
        self.status = 0 # 0 - Disponível; 1 - Ocupado; 2 - Em espera
        self.esperaClientes = [] # Clientes que estão esperando para assistir o filme.

    # Se a quantidade de clientes assistindo for menor que o limite então há limites.
    def haVagas(self): return len(self.clientes) < self.limite

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            
            while True:
                try:
                    self.socket = s
                    self.socket.bind((self.host, self.port))
                    self.socket.listen()
                    break
                except OSError:
                    print(f"Porta {self.port} já está em uso! Aguardando 5 segundos...")
                    sleep(5)

            print(f"Vídeo {self.id} escutando em {self.host}:{self.port}")

            try:
                while True:
                    conn, addr = self.socket.accept()
                    print(f"Conectado a {addr}")
                    dados = conn.recv(1024)
                    self.thrs.append(Thread(target=self.sel, args=(dados.decode(), conn, addr,)))
                    self.thrs[-1].start()
                    
            except KeyboardInterrupt:
                print("\nEncerrando...")

    def sel(self, dados:str, conn:socket.socket, addr:tuple):
        lista = dados.split(";")
        op = int(lista[0])
        if op == 1:
            self.rodarOrq(conn, addr, dados)
        elif op == 2:
            self.rodarCliente(conn, addr, dados)
    

    def rodarOrq(self, conn:socket.socket, addr:tuple, dados:str):
        self.orq = (conn, addr)
        print(f"Dados recebidos do cliente: {dados}")
        conn.sendall(f"{self.limite}".encode()) # Envia o limite de clientes definido

        count = 5
        while count > 0:
            self.atendimento(conn, addr)
            count -= 1

    def rodarCliente(self, conn:socket.socket, addr:tuple, dados:str):
        print(f"Dados recebidos do cliente: {dados}")
        # Dados virão no formato: id_orqCliente;host;port;distancia
        idC, distancia = dados.split(";")
        cliente = VidCliente(
            id=int(idC),
            host=addr[0],
            port=int(addr[1]),
            distancia=float(distancia),
            conn=conn,
            addr=addr
        )
        self.addCliente(cliente)
        

    def atendimento(self, conn:socket.socket, addr:tuple):
        
        print('Atendimento. Esperando receber algo...')
        rCabecalho = conn.recv(1024)
        cabecalho = rCabecalho.decode()
        print(f"Cabecalho recebido: {cabecalho}")

        idF, nome, duracao, genero, ano = cabecalho.split(";")

        self.filme = VidFilme(
            id=int(idF),
            nome=nome,
            duracao=int(duracao),
            genero=genero,
            ano=int(ano)
        )
        
        dados = []
        f = ""

        while "#" not in f:
            rDados = conn.recv(1024)
            f = rDados.decode()
            if "#" not in f: 
                dados.append(int(f))
                print(f"Recebido do filme {self.filme}: {f}/{self.filme.duracao}.")
        
        self.filme.dados = dados
        
        print(f"Filme {self.filme} recebido!\n")


    def transmitir(self, cliente:VidCliente):
        print(f"Transmitindo filme {self.filme} para o cliente {cliente.id}...")
        cliente.enviar(self.filme) # Filme é transmitido ao cliente.
        

    def addCliente(self, cliente:VidCliente):
        while True:
            if self.haVagas():
                self.clientes.append(cliente)
                print(f"Cliente {cliente.id} adicionado à lista de clientes do vídeo {self.id}.")
                self.transmitir(cliente)
                self.removeCliente(cliente) # Cliente é removido da lista de clientes do vídeo.
                break
            else:
                print(f"Não há vagas para o cliente {cliente.id} no vídeo {self.id}. Adicionando à lista de espera...")
                sleep(5)

    def removeCliente(self, cliente:VidCliente):
        for i in range(len(self.clientes)):
            if self.clientes[i].id == cliente.id:
                self.clientes.pop(i)
                break
        print(f"Cliente {cliente.id} removido da lista de clientes do vídeo {self.id}.")
        self.orq[0].sendall(f"{3};{cliente.id}".encode()) # Envia para a orquestradora que o cliente saiu.



        

        

        


                

        