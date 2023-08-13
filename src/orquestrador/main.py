import socket
from threading import Thread
from time import sleep
from conector import Conector
from orqStream import OrqStream
from orqVideo import OrqVideo
from orqCliente import OrqCliente
from orqFilme import OrqFilme
from math import sqrt

class Orq(Conector):

    def __init__(
        self,
        host:str="localhost",
        port:int=3000,
        hostStr:str="localhost",
        portStr:int=5000,
        hostVid:str="localhost",
        portVid:int=4000,
    ):
        self.hostStr = hostStr
        self.portStr = portStr
        self.hostVid = hostVid
        self.portVid = portVid
        self.stream:OrqStream = OrqStream(hostStr, portStr)
        self.videos:list = None
        self.clientes:list = []
        self.thrs = []
        self.filme:OrqFilme = None
        super().__init__(host, port)


    def fechaTudo(self):
        self.stream.fechar()
        for v in self.videos:
            v.fechar()
        for c in self.clientes:
            c.fechar()
        self.fechar()
        print("\n----- 2 - Servidor encerrado -----\n")
        exit()

    def run(self):
        try:
            self.conectaStream()
            self.conectaVideos()
            self.iniciarOrq()
            
        except (KeyboardInterrupt, BrokenPipeError) as e:
            print("\n----- 1 - Servidor encerrado -----\n")
            print('Erro dado: ', e)
            self.fechaTudo()

    def conectaStream(self):
        self.stream = OrqStream(self.hostStr, self.portStr)
        self.stream.run()
        
    def conectaVideos(self):
        posicoes = [(2, 6)]
        self.videos = [OrqVideo(self.hostVid, self.portVid + i, x=p[0], y=p[1]) for i, p in enumerate(posicoes, 1) ]
        for v in self.videos: 
            v.run()
        
    def iniciarOrq(self):
        self.rodarServ()
        self.escutar()

    def escutar(self):
        while True:
            conn, addr = self.conn.accept()
            print(f"\n-- Conexão estabelecida com cliente ({addr}) --\n")
            cliente = OrqCliente(conn=conn, addr=addr)
            self.clientes.append(cliente)
            nova = Thread(target=self.atendimento, args=(cliente,))
            self.thrs.append(nova)
            nova.start()
    
    def atendimento(self, cliente:OrqCliente):
        try:
            print(f"\nAtendimento iniciado... ao cliente {cliente.id}\n")
            cliente.inicializacao(self.videos) # Função que fará etapas iniciais do cliente
            self.gerExibicaoFilmes(cliente) # Função que fará a exibição de filmes para o cliente

        except (KeyboardInterrupt, ConnectionResetError) as e:
            print("Conexão com cliente encerrado!")
            print(f"Erro dado: {e}")
            self.fechaTudo()
            return

    def gerExibicaoFilmes(self, cliente:OrqCliente):
        op = -1
        while op != 0:
            op = self.menu(cliente) # Requisita, recebe o menu do STREAM e depois envia ao CLIENTE
            self.selecao(cliente, op) # Recebe a seleção do cliente e segue as funções de acordo com a opção

    def menu(self, cliente:OrqCliente):
        menu = self.stream.receberMenu()
        cliente.enviarMenu(menu)
        op = cliente.receberInt()
        print(f"-- Opção recebida: {op} - {type(op)} --")
        return op
        
    def selecao(self, cliente:OrqCliente, op:int):
        if op == 0:
            # Encerrar conexão com cliente
            cliente.fechar()
        else:
            self.transmitir(cliente, op)

    def transmitir(self, cliente:OrqCliente, op:int):
        video, caso = self.selecionarVideo(cliente, op)
        self.selecionarCaso(cliente, video, caso, op)
        
    def selecionarVideo(self, cliente:OrqCliente, op:int):
        vidSel = None
        caso = -1

        # Caso = 1: Há algum vídeo transmitindo o filme, verifica se há vagas
        # Caso = 2: Não há nenhum vídeo transmitindo o filme, verifica se há vídeos disponíveis

        while vidSel == None:
            comFilme, comStatus = self.buscaVideo(op, 0) # Busca o vídeo que já esteja transmitindo o filme.            
            if len(comFilme) > 0:
                # Tem algum vídeo transmitindo o filme:
                # No caso, verifica se há vagas nele.
                vidSel = self.pertoComVaga(cliente, comFilme)
                caso = 1
            elif len(comStatus) > 0:
                # Não tem nenhum vídeo transmitindo o filme:
                vidSel = self.pertoComVaga(cliente, comStatus)
                caso = 2
            else:
                print("Não há videos transmitindo esse filme e nem videos disponíveis.")
                print("Aguardando 5 segundos para verificar novamente.")
                sleep(5)
        
        return vidSel, caso

    def buscaVideo(self, idFilme:int=None, status:int=None):
        comFilme, comStatus = [], []
        
        for v in self.videos:
            if idFilme is not None and v.filme is not None:
                if v.filme.id == idFilme:
                    comFilme.append(v)
            
            if status is not None:
                if v.status == status:
                    comStatus.append(v)

        return comFilme, comStatus

    def pertoComVaga(self, cliente:OrqCliente, videos:list) -> OrqVideo:
        l = [ v for v in self.maisPerto(cliente, videos) if v['video'].haVaga() ]
        return l[0] if len(l) > 0 else None
                
    def maisPerto(self, cliente:OrqCliente, videos:list):
        distancias = []
        for v in videos:
            distancias.append({'video': v, 'distancia': cliente.buscaDistancia(v.id)})
        distancias.sort(key=lambda x: x['distancia'])
        print(distancias)
        return distancias
    
    def selecionarCaso(self, cliente:OrqCliente, video:dict=None,  caso:int=None, op:int=None):
        # Caso = 1: O video está transmitindo esse filme e há vagas
        # Caso = 2: Não há nenhum vídeo transmitindo o filme, mas ele é o mais proximo.
        # video: {'video': OrqVideo, 'distancia': float}
        if caso == 1: 
            print(f"Caso {caso}. Transmitindo o filme {video['video'].filme.id}; O cliente {cliente.id} irá se conectar.")
            pass
        elif caso == 2: 
            print(f"Caso {caso}. O Video ainda não transmite. Mas transmitirá e o cliente depois irá se conectar.") 
            self.iniciaTransmissao(video['video'], op)
            pass

    def iniciaTransmissao(self, video:OrqVideo, op:int):
        # Nessa função o filme será solicitado ao STREAM e depois será transmitido ao VIDEO
        self.filme = self.stream.recebeFilme(op)
        print("Filme: ", self.filme)
        print(self.filme.dados)



if __name__ == "__main__":
    orq = Orq()
    orq.run()



