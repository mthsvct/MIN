from posicoes import Posicoes
from hostPort import HostPort
import socket
from time import sleep



class Video(HostPort, Posicoes):

    total = 0

    def __init__(
            self,
            host:str, port:int,
            x:int, y:int,
            idFilme:int=-1,
            status:str="espera",
            limite:int=3,
            numClientes:int=0,
            conn:socket.socket=None,
            addr:tuple=None,
            filme:list=[]
        ) -> None:

        self.id = Video.total
        Video.total += 1

        self.idFilme = idFilme
        self.status = status
        self.limite = limite
        self.numClientes = numClientes
        self.clientes = [] # lista de ids de clientes
        self.conn = conn
        self.addr = addr

        self.filme = [] # Buffer que será transmitido para os vídeos para que depois seja transmitido para os clientes.
        
        HostPort.__init__(self, host, port)
        Posicoes.__init__(self, x, y)

    def __str__(self): return f"Video:{self.id}\nAddr:{self.addr}\nPosicao:{self.x},{self.y}"

    # Retorna True se o número de clientes assistindo o filme for menor que o limite
    # Retorna False se o número de clientes assistindo o filme for igual ao limite
    def haVaga(self): return self.numClientes < self.limite

    def run(self):
        # Informar que está conectado ao orquestrador
        self.conn.sendall(b"Conectado ao orquestrador com sucesso. filmeId: " + str(self.idFilme).encode())

        
    
    def addCliente(self, cliente):
        self.clientes.append(cliente.id)
        self.numClientes += 1
    
    def transmitir(self):
        # Função que transmite algo para o endereço.
        pass

    def transmiteFilme(self, cliente, idFilme, cabecalho:str):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # Transmitir o filme para o video
            s.connect(self.addr)
            self.idFilme = idFilme
            self.status = "transmitindo filme para video"
            s.sendall(cabecalho.encode())
            print("Cabeçalho do filme enviado para o video...")
            sleep(1)
        


    

