import socket
from math import sqrt
from time import sleep

from threading import Thread
from orqVideo import OrqVideo
from orqCliente import OrqCliente
from orqStream import OrqStream as Stm

class Orquestrador:

    def __init__(self, host="localhost", port=2000, hostStream="localhost", portStream=4001, hostVideos="localhost", portVideos=3000):
        self.host = host
        self.port = port
        self.socket = None
        self.hostStream = hostStream
        self.portStream = portStream
        self.stream = None
        self.hostVideos = hostVideos
        self.portVideos = portVideos
        self.thrStream = None
        self.videos = []
        self.thrsVideos = [] # Threads de conexões de vídeos
        self.thrs = []
        self.distancias = []
        self.clientes = []
        self.espera = [] # Requisições de filmes a serem assistidos.

    def run(self):
        self.conectaStream()
        self.conectaVideos()
        self.conectaClientes()
    
    def conectaStream(self):
        self.stream = Stm(self.hostStream, self.portStream)
        self.thrStream = Thread(target=self.stream.run)
        self.thrStream.start()
    
    def conectaVideos(self):
        pos = [(2, 6)]
        self.videos = [ OrqVideo(self.host, self.portVideos + i, x=pos[i-1][0], y=pos[i-1][1]) for i in range(1,2) ]
        for i in self.videos: print(i.port)
        self.thrsVideos = [ Thread(target=video.run) for video in self.videos ]
        for thr in self.thrsVideos: thr.start()

    def conectaClientes(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            
            while True:
                try:
                    s.bind((self.host, self.port))
                    break
                except OSError:
                    print("Orquestrador não pode rodar! CLIENTE espere. Aguardando 5 segundos...")
                    sleep(5)

            s.listen()
            print(f"Orquestrador escutando em {self.host}:{self.port}")

            try:
                while True:
                    conn, addr = s.accept()
                    novo = OrqCliente(conn=conn, addr=addr)
                    self.thrs.append(Thread(target=self.runCliente, args=(novo,)))
                    self.thrs[-1].start()

            except (ValueError, KeyboardInterrupt) as e:
                print("\nEncerrando...!", e)
                # for thr in self.thrs: thr.join()
                # for thr in self.thrsVideos: thr.join()
                # self.thrStream.join()

    def runCliente(self, novo:OrqCliente):

        print(f"Cliente com id {novo.id} e endereco {novo.addr} conectado!")

        dados = novo.conn.recv(1024)
        print(f"Dados recebidos do cliente {novo.id}: {dados.decode()}")

        lista = dados.decode().split(";")
        novo.x, novo.y = int(lista[0]), int(lista[1])
        self.calcularDistancias(novo)

        print(f"Cliente possui as seguintes coordenadas: ({novo.x}, {novo.y})")
        self.clientes.append(novo)

        novo.conn.sendall(b"Dados recebidos! Obrigado!")
        self.transmitirFilmes(novo)

    def calcularDistancias(self, cliente:OrqCliente):

        for video in self.videos:
            x1, y1 = cliente.x, cliente.y
            x2, y2 = video.x, video.y
            distancia = sqrt((x2 - x1)**2 + (y2 - y1)**2)
            self.distancias.append({'C': cliente.id, 'V': video.id, 'D': round(distancia, 2)})

    def transmitirFilmes(self, cliente:OrqCliente):
        op = -1
        while op != 0:
            m = self.stream.menu()
            cliente.conn.sendall(m)
            print("Menu enviado ao CLIENTE.")

            resOp = cliente.conn.recv(1024) # Recebe a opção escolhida pelo cliente. IdFilme
            
            print(f"RespOp: {resOp.decode()}")

            op = int(resOp.decode())
            print(f"Opção escolhida pelo CLIENTE: {op}")

            if op != 0:
                self.selectVideo(cliente, op)

        print(f"Encerrando conexão com cliente de endereco {cliente.id} {cliente.addr}")

    def selectVideo(self, cliente:OrqCliente, op:int):
        while True:
            videoComFilme, videosDisponiveis = self.buscaVideoFilme(op)

            if videoComFilme != None:
                # Existe um vídeo que transmitindo o filme desejado.
                print(f"Existe um vídeo que transmite o filme desejado. vagas: {videoComFilme.haVagas()}")

                # Verifica se o video possui vagas
                if videoComFilme.haVagas():
                    # Apenas adiciona o cliente na lista de clientes do vídeo.
                    videoComFilme.addCliente(cliente)
                    cliente.conn.sendall(f"{videoComFilme.host};{videoComFilme.port};{dis};{cliente.id}".encode())
                    print(f"Vídeo mais próximo encontrado. {v}")
                    break
                
                else:
                    # Verifica se existe um vídeo mais próximo que possui vagas. <- ISSO EU NÃO VOU FAZER
                    # Colocar o cliente na lista de espera do Video
                    # Assim que o Video termina de transmitir um filme para um cliente ele verifica a lista de espera
                    # Se houver clientes na espera ele começa a transmitir o filme para o cliente que está na espera.
                    # Caso não haja, ele manda sinal de subtração para o orquestrador. Informando que o número de clientes assistindo diminuiu.
                    print("EXISTE 1 vídeo transmitindo o filme desejado, porém não há vagas nele ainda. Aguardando...")
                    sleep(5)

            else:
                print("Não existe um vídeo que transmite o filme desejado.")
                
                if len(videosDisponiveis) == 0:
                    # Não existe nenhum vídeo disponível para transmitir o filme desejado.
                    # Logo, deve ser armazenado em uma lista de espera.
                    print("Não existe nenhum vídeo disponível para transmitir o filme desejado.")
                    sleep(5)
                    
                else:
                    # Se existir videos disponíveis, logo fazer a busca do ideal. (Mais próximo do cliente)
                    dis, v = self.maisPerto(cliente, videosDisponiveis)
                    print(f"Vídeo mais próximo encontrado. {v}")
                    filme = self.stream.recebeFilme(op)
                    v.filme = filme
                    v.enviarFilme()




    def buscaVideoFilme(self, idFilme:int) -> OrqVideo:
        videosComFilme = None
        for i in self.videos:
            if i.filme != None and i.filme.id == idFilme:
                videosComFilme = i
                break
        videosDisponiveis = [ video for video in self.videos if len(video.clientes) == 0 ] # Quando não há clientes assistindo o vídeo.
        return videosComFilme, videosDisponiveis
    
    def addListaEspera(self, cliente:OrqCliente, op:int):
        self.espera.append( { "cliente": cliente, "op": op })
        cliente.conn.sendall("Infelizmente não há vídeos disponíveis para transmitir o filme desejado no momento. Você foi adicionado a lista de espera.".encode())

    def maisPerto(self, cliente:OrqCliente, videosDisponiveis:list):
        # d = [ self.buscaDistancia(cliente.id, video.id) for video in videosDisponiveis ]
        perto = []
        for video in videosDisponiveis:
            d = self.buscaDistancia(cliente.id, video.id)
            if len(perto) == 0 or d < perto[0]:
                perto = [d, video]
        return perto 
        
    def buscaDistancia(self, idCliente:int, idVideo:int) -> float:
        return [ i['D'] for i in self.distancias if i['C'] == idCliente and i['V'] == idVideo ][0]

