import socket
from time import sleep
from orqCliente import OrqCliente
from orqFilme import OrqFilme

class OrqVideo:

    # Funções que envia e recebe sinais a um vídeo do orquestrador.
    
    id = 1

    def __init__(self, host:str='localhost', port:int=3000, x=0, y=0, limite:int=3):
        self.id = OrqVideo.id
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.x = x
        self.y = y
        self.clientes = []
        self.clientesEspera = []
        self.limite = limite
        self.filme:OrqFilme = None
        OrqVideo.id += 1
    
    def run(self):
        while True:
            try:
                self.socket.connect((self.host, self.port)) # Conecta ao vídeo
                break
            except ConnectionRefusedError:
                print("Servidor de vídeos não está ativo! Aguardando 5 segundos...")
                sleep(5)

        self.socket.sendall(f"1;{self.x};{self.y}".encode())
        limite = self.socket.recv(1024)
        print("Limite recebido: ", limite.decode())
        self.limite = int(limite)


    # Se a quantidade de clientes assistindo for menor que o limite então há limites.
    def haVagas(self): return len(self.clientes) < self.limite


    def addCliente(self, cliente:OrqCliente): 
        self.clientes.append(cliente)
        cliente.video = self
        print(f"Cliente {cliente.id} adicionado ao vídeo {self.id}.")


    def rmCliente(self, cliente:OrqCliente):
        self.clientes.remove(cliente)
        cliente.video = None
        print(f"Cliente {cliente.id} removido do vídeo {self.id}.")


    def addClienteEspera(self, cliente:OrqCliente): 
        pass
    
    def enviarFilme(self): 
        self.socket.sendall(self.filme.cabecalho.encode())
        print("ORQUESTRADOR enviou o cabeçalho do filme para o VIDEO.")

        for frame in self.filme.dados:
            self.socket.sendall(str(frame).encode())
            print(f"ORQUESTRADOR enviou um frame para o VIDEO: {frame} / {self.filme.duracao}")
            sleep(0.1)
        
        self.socket.sendall("#".encode())
        print(f"ORQUESTRADOR enviou o filme {self.filme} para o VIDEO.")

        self.aguardar()

    def aguardar(self):

        while True:
            # Receber a instrução de que Láááá no vídeo aconteceu:
            # 1 - Um novo cliente entrou e está assistindo (Adicionar o cliente na lista de clientes)
            # 2 - Um novo cliente entrou e está esperando (Adicionar o cliente na lista de espera)
            # 3 - Um cliente saiu. (Buscar o cliente o id e remover aqui na lista de clientes)
            # 4 - Não há mais nenhum cliente assistindo. (Remover o filme da memória)
            break




        


