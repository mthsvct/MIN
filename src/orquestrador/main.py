import socket
from threading import Thread, Lock
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
        self.videos:dict = {
            "comFilme": [],
            "semFilme": []
        }
        self.clientes:list = []
        self.thrs = []
        self.filmes:list = []
        self.ocupados:list = []
        self.lock:Lock = Lock()
        super().__init__(host, port)

    
    def convertePraLista(self):
        return self.videos['comFilme'] + self.videos['semFilme']


    def fechaTudo(self):
        self.stream.fechar()
        for v in self.convertePraLista():
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
        posicoes = [(2, 6), (3, 1)]
        self.videos['semFilme'] = [ OrqVideo(self.hostVid, self.portVid + i, x=p[0], y=p[1]) for i, p in enumerate(posicoes, 1) ]
        for v in self.convertePraLista(): 
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
        # try:
        print(f"\nAtendimento iniciado... ao cliente {cliente.id}\n")
        cliente.inicializacao(self.convertePraLista()) # Função que fará etapas iniciais do cliente
        self.gerExibicaoFilmes(cliente) # Função que fará a exibição de filmes para o cliente

        # except (KeyboardInterrupt, ConnectionResetError) as e:
        #     print("Conexão com cliente encerrado!")
        #     print(f"Erro dado: {e}")
        #     self.fechaTudo()

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
        self.selecionarCaso(cliente, video['video'], video['distancia'], caso, op)
        
    def selecionarVideo(self, cliente:OrqCliente, op:int):
        vidSel = None
        caso = -1

        # Caso = 1: Há algum vídeo transmitindo o filme, verifica se há vagas
        # Caso = 2: Não há nenhum vídeo transmitindo o filme, verifica se há vídeos disponíveis

        while vidSel == None:

            comFilme, comStatus, comFilmeEStatus = self.buscaVideo(idFilme=op, status=0) # Busca o vídeo que já esteja transmitindo o filme. 

            print()            
            print("Com filme: ", comFilme)
            print("Com status: ", comStatus)
            print("Com filme e status: ", comFilmeEStatus)
            print()
            
            if len(comFilme) > 0:
                # Tem algum vídeo transmitindo o filme:
                # No caso, verifica se há vagas nele.
                vidSel = self.pertoComVaga(cliente, comFilme)
                caso = 1

            elif len(comStatus) > 0:
                # Não tem nenhum vídeo transmitindo o filme:
                vidSel = self.pertoComVaga(cliente, comStatus)
                caso = 2
                vidSel['video'].filme = OrqFilme(op)
                vidSel['video'].clientes.append(cliente)
                self.videos['comFilme'].append(vidSel['video'])
                self.videos['semFilme'].remove(vidSel['video'])

            elif len(comFilmeEStatus) > 0:
                vidSel = self.pertoComVaga(cliente, comFilmeEStatus)
                vidSel['video'].filme = OrqFilme(id=op)
                vidSel['video'].clientes.append(cliente)
                caso = 2

            else:
                print("Não há videos transmitindo esse filme e nem videos disponíveis.")
                print("Aguardando 5 segundos para verificar novamente.")
                sleep(5)



        print(f"Vídeo selecionado: {vidSel['video'].id} - {vidSel['video'].filme} - {vidSel['distancia']}")
        print(f"--------------- CASO: {caso} ---------------")

        

        return vidSel, caso

    def buscaVideo(self, idFilme:int=None, status:int=0):        

        comFilme = []
        for v in self.videos['comFilme']:
            print(f"{v.filme} == {idFilme} : {v.filme == None}")
            if v.filme != None:
                print(f"{v.filme.id} == {idFilme} : {v.filme.id == idFilme}")
                if v.filme.id == idFilme:
                    comFilme.append(v)
        
        comStatus = []
        for v in self.videos['semFilme']:
            if v.status == status and v.filme == None:
                comStatus.append(v)
                
        
        comFilmeEStatus = []
        for v in self.convertePraLista():
            if v.status == status and (v.filme != None and v.filme.id != idFilme) and len(v.clientes) == 0:
                comFilmeEStatus.append(v)

        
        return comFilme, comStatus, comFilmeEStatus

    def pertoComVaga(self, cliente:OrqCliente, videos:list) -> OrqVideo:
        proximos = self.maisPerto(cliente, videos)
        for v in proximos:
            if v['video'].haVaga()[0]:
                return v
        return None
                
    def maisPerto(self, cliente:OrqCliente, videos:list):
        distancias = []
        for v in videos:
            distancias.append({'video': v, 'distancia': cliente.buscaDistancia(v.id)})
        distancias.sort(key=lambda x: x['distancia'])
        print("Distancias: ", distancias)
        return distancias
    
    def selecionarCaso(self, cliente:OrqCliente, video:OrqVideo=None, distancia:float=None, caso:int=None, op:int=None):
        # Caso = 1: O video está transmitindo esse filme e há vagas
        # Caso = 2: Não há nenhum vídeo transmitindo o filme, mas ele é o mais proximo.
        # video: {'video': OrqVideo, 'distancia': float}
        # print("\n--------\n", video, distancia, caso, op)

        if caso == 1: 
            #print(f"Caso {caso}. Transmitindo o filme {video.filme}; O cliente {cliente.id} irá se conectar.")
            print(f"Caso 1. Transmitindo o filme {video.filme}; O cliente {cliente.id} irá se conectar.")
            self.exibirFilme(cliente, video, distancia)

        elif caso == 2: 
            print(f"Caso {caso}. O Video ainda não transmite. Mas transmitirá e o cliente depois irá se conectar.") 
            video = self.iniciaTransmissao(video, op)
            self.selecionarCaso(cliente, video, distancia, 1, op)


    def estar(self, idVideo:int):
        retorno = False
        for i in self.ocupados:
            if i == idVideo:
                retorno = True
                break
        return retorno

    def iniciaTransmissao(self, video:OrqVideo, op:int):
        # Nessa função o filme será solicitado ao STREAM e depois será transmitido ao VIDEO
        filme = self.stream.recebeFilme(op)
        video.filme = filme
        self.filmes.append(video.filme)
        video.transmitirFilme(video.filme)
        return video
        
    def exibirFilme(self, cliente:OrqCliente, video:OrqVideo, distancia:float=1.0):
        cliente.enviar(f"{video.host};{video.port};{distancia};")
        sinal = video.receberLista()
        video.transmitindo = True

        idCliente = int(sinal[0])
        status = int(sinal[1])
        qntClientes = int(sinal[2])
        idFilme = int(sinal[3])

        video.status = status
        # video.clientes.append(cliente)

        print(f"->>> Sinal recebido: {sinal}. <<<-")

        sinalEncerramento = video.receberLista() # Virá um sinal com: id do cliente, status e qnt clientes no momento. 
        print(f"->>> Sinal de ENCERRAMENTO recebido: {sinalEncerramento}. <<<-")
        video.clientes.remove(cliente)
        video.status = int(sinalEncerramento[1])
        video.transmitindo = False
        print(f"QNT CLIENTES: {sinalEncerramento[2]}, {len(video.clientes)}, {len(video.clientes) == int(sinalEncerramento[2])}")
    

if __name__ == "__main__":
    orq = Orq()
    orq.run()



