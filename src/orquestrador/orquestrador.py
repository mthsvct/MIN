from hostPort import HostPort
from videoO import Video
from clienteO import Cliente
from servidorO import Servidor

import socket
from threading import Thread
from time import sleep
from math import sqrt

# tipo = 1 == Cliente
# tipo = 2 == Video
# tipo = 3 == Servidor

class Orquestrador(HostPort):

    def __init__(
        self, host:str, port:int,
        hostServer:str="localhost", 
        portServer:int=3000,
        tabelaPosicoes:list=[],
        clientes:list=[],
        videos:list=[],
        filaEspera:list=[],
    ):
        self.hostServer = hostServer
        self.portServer = portServer
        self.tabelaPosicoes = tabelaPosicoes
        self.clientes = clientes
        self.videos = videos
        self.filaEspera = filaEspera
        self.thrs = []
        self.servidor = Servidor()
        super().__init__(host, port)

    def tipo(self, t:int): 
        return (["Cliente", "Video", "Servidor"][t-1], t) if (t > 0 and t < 4) else "Erro ao receber tipagem do dispositivo."

    def start(self):
        self.servidor.run() # Testa a conexão com o servidor.

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as orqS:
            orqS.bind((self.host, self.port))
            orqS.listen()
            print("Orquestrador aguardando conexoes...")
            while True:
                conn, addr = orqS.accept()
                self.thrs.append(Thread(target=self.rodar, args=(conn, addr)))
                self.thrs[-1].start()


    def rodar(self, conn, addr):
        with conn:
            r = conn.recv(1024)
            t, x, y = r.decode().split(";")
            tipo = self.tipo(int(t)) if r else "Erro ao receber tipagem do dispositivo."
            self.select(tipo[1], int(x), int(y), conn, addr)


    def select(self, tipo:int, x:int, y:int, conn, addr):

        if tipo == 1:
            print(f"Cliente com o endereço {addr} conectado.")
            novo = Cliente(host=addr[0],port=addr[1],x=x,y=y,conn=conn,addr=addr)
            self.calculaDistancias(novo)
            self.clientes.append(novo)
            
            for i in self.tabelaPosicoes: 
                print(f"Distancia de {i['C']} para {i['V']} é {i['D']}")

            novo.run(self.servidor.menu(), self)
            self.solicitaFilme(novo, novo.idFilme)
            
        elif tipo == 2:
            print(f"Video com o endereço {addr} conectado.")
            novo = Video(host=addr[0],port=addr[1], x=x, y=y, conn=conn, addr=addr)
            self.videos.append(novo)
            novo.run()

            for i in self.videos:
                print(i.id, i.status)

    
    def solicitaFilme(self, cliente:Cliente, idFilme:int):
        # No caso do meu programa, dois vídeos podem transmitir o mesmo filme.
        # Verificar se há algum vídeo que esteja passando o filme.
        #   Se houver, enviar o cabeçalho do filme para o cliente.
        
        # Cabecalho: "1;Kill Bill;95;2003"
        # Desc: "id;nome;duracao;ano"

        vs, tam = self.buscaVideo(idFilme)

        print(f"Quantidade de vídeos disponíveis: {tam}")
        print(f"Vídeos disponíveis: {vs}")

        if tam > 0:
            # Se houver vídeos disponíveis, ir para a função de seleção de vídeo.
            video = self.selecionaVideo(cliente, idFilme, vs)
        else:
            # Se não houver vídeos disponíveis, colocar o cliente na fila de espera.
            self.filaEspera.append( (cliente.id, idFilme) )

        

    def buscaVideo(self, idFilme):
        # Retorna se um dicionário com os vídeos que possuem o filme e os que não possuem.
        vs = [ i for i in self.videos if i.haVaga() ]
        possuiFilme = [ i for i in vs if i.idFilme != -1 ]
        semFilme = [ i for i in vs if i.idFilme == -1 ]
        return { "possuiFilme": (possuiFilme, len(possuiFilme)), "semFilme": (semFilme, len(semFilme)) }, len(vs)

    
    def calculaDistancias(self, novo:Cliente):
        for i in self.videos:
            distancia = sqrt(((i.x - novo.x) ** 2) + ((i.y - novo.y) ** 2))
            self.tabelaPosicoes.append({"C":novo.id, "V":i.id, "D":round(distancia, 2)})


    def selecionaVideo(self, cliente:Cliente, idFilme:int, vs:dict):
        # Seleciona o vídeo para que a transmissão do filme seja feita para o cliente.
        #   Associa as distancias
        distancias = []

        

        for i in vs['possuiFilme'][0]:
            print(i)
            for j in self.tabelaPosicoes:
                if j['V'] == i.id and j['C'] == cliente.id:
                    distancias.append({'video': i, 'distancia': j['D'], 'possuiFilme': True})
        
        for i in vs['semFilme'][0]:
            for j in self.tabelaPosicoes:
                if j['V'] == i.id and j['C'] == cliente.id:
                    distancias.append({'video': i, 'distancia': j['D'], 'possuiFilme': False})
        
        distancias.sort(key=lambda x: x['distancia'])
        
        if distancias[0]['possuiFilme']:
            distancias[0]['video'].addCliente(cliente)
        else:
            distancias[0]['video'].transmiteFilme(cliente, idFilme, self.servidor.cabecalho(idFilme))

