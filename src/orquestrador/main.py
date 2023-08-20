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
            conn, addr = self.conn.accept() # Aceita a conexão
            print(f"\n-- Conexão estabelecida com cliente ({addr}) --\n")
            cliente = OrqCliente(conn=conn, addr=addr) # Cria um objeto cliente
            self.clientes.append(cliente) # Adiciona o cliente na lista de clientes
            nova = Thread(target=self.atendimento, args=(cliente,)) # Cria uma thread para atender o cliente
            self.thrs.append(nova) # Adiciona a thread na lista de threads
            nova.start() # Inicia a thread
    

    def atendimento(self, cliente:OrqCliente):
        print(f"\nAtendimento iniciado... ao cliente {cliente.id}\n")
        cliente.inicializacao(self.convertePraLista()) # Função que fará etapas iniciais do cliente
        self.gerExibicaoFilmes(cliente) # Função que fará a exibição de filmes para o cliente

        

    def gerExibicaoFilmes(self, cliente:OrqCliente):
        op = -1
        while op != 0:
            op = self.menu(cliente) # Requisita, recebe o menu do STREAM e depois envia ao CLIENTE
            self.selecao(cliente, op) # Recebe a seleção do cliente e segue as funções de acordo com a opção


    def menu(self, cliente:OrqCliente):
        menu = self.stream.receberMenu() # Recebe o menu do STREAM
        cliente.enviarMenu(menu) # Envia o menu ao CLIENTE
        op = cliente.receberInt() # Recebe a opção do CLIENTE
        print(f"-- Opção recebida: {op} - {type(op)} --")
        return op # Retorna a opção para a função gerExibicaoFilmes
        

    def selecao(self, cliente:OrqCliente, op:int):
        if op == 0:
            # Encerrar conexão com cliente
            cliente.fechar()
        else:
            # Transmitir filme
            self.transmitir(cliente, op)

    def transmitir(self, cliente:OrqCliente, op:int):
        video, caso = self.selecionarVideo(cliente, op) # Seleciona o vídeo que irá transmitir o filme. Caso é o tipo de caso que ocorreu.
        self.selecionarCaso(cliente, video['video'], video['distancia'], caso, op) # Seleciona o caso que ocorreu e segue com as funções de acordo com o caso.
        
    def selecionarVideo(self, cliente:OrqCliente, op:int):
        vidSel = None # Vídeo selecionado
        caso = -1 # Caso que ocorreu

        while vidSel == None: # Enquanto não selecionar um vídeo, irá repetir o processo.

            comFilme, comStatus, comFilmeEStatus = self.buscaVideo(idFilme=op, status=0) # Busca o vídeo que já esteja transmitindo o filme. 

            if len(comFilme) > 0:
                # Tem algum vídeo transmitindo o filme:
                # No caso, verifica se há vagas nele.
                print("-------- ENTROU NESTE CASO --------")
                vidSel = self.pertoComVaga(cliente, comFilme) # Seleciona o vídeo mais próximo que tenha vaga.
                print(f"\n-------- VÍDEO SELECIONADO: {vidSel['video'].id} --------\n")
                vidSel['video'].clientes.append(cliente) # Adiciona o cliente na lista de clientes do vídeo.
                caso = 1 # Caso 1: O vídeo já transmite o filme e há vagas.

                while self.stream.blocked == True:
                    print("\n ++++++ O ORQ ainda está recebendo este filme. Aguarde um momento. Por favor. \n")
                    sleep(3)
                
                while self.videos['comFilme'][self.videos['comFilme'].index(vidSel['video'])].recebendo == True:
                    print("\n ****** O vídeo ainda está recebendo o filme. por favor aguarde ")
                    sleep(1.2)

                while self.videos['comFilme'][self.videos['comFilme'].index(vidSel['video'])].limite + 1 <= len(self.videos['comFilme'][self.videos['comFilme'].index(vidSel['video'])].clientes):
                    print("\n ++++++ O vídeo está lotado. Aguarde um momento. Por favor.")
                    sleep(3)
                    
                    
            elif len(comStatus) > 0:
                # Não tem nenhum vídeo transmitindo o filme:
                vidSel = self.pertoComVaga(cliente, comStatus) # Seleciona o vídeo mais próximo que não esteja transmitindo o filme.
                caso = 2 # Caso 2: Não há nenhum vídeo transmitindo o filme, mas ele é o mais proximo.
                vidSel['video'].filme = OrqFilme(op) # Adiciona o filme ao vídeo.
                vidSel['video'].clientes.append(cliente) # Adiciona o cliente na lista de clientes do vídeo.
                self.videos['comFilme'].append(vidSel['video']) # Adiciona o vídeo na lista de vídeos que transmitem o filme.
                self.videos['semFilme'].remove(vidSel['video']) # Remove o vídeo da lista de vídeos que não transmitem o filme.

            elif len(comFilmeEStatus) > 0:
                # Possui um filme, mas pode ser substituido pq não tem clientes assistindo.
                vidSel = self.pertoComVaga(cliente, comFilmeEStatus) # Seleciona o vídeo mais próximo que não esteja transmitindo o filme.
                vidSel['video'].filme = OrqFilme(id=op) # Adiciona o filme ao vídeo.
                vidSel['video'].clientes.append(cliente) # Adiciona o cliente na lista de clientes do vídeo.
                caso = 2 # Caso 2: Esse vídeo possui um filme, mas como não tem nenhum cliente assistindo então o filme pode ser substituido.

            else:
                # Não tem nenhum vídeo transmitindo o filme e nem tem nenhum vídeo disponível.
                print("\nNão há videos transmitindo esse filme e nem videos disponíveis.")
                print("Aguardando 5 segundos para verificar novamente.\n")
                sleep(3) # Aguarda 2 segundos para verificar novamente.

        return vidSel, caso # Retorna o vídeo selecionado e o caso que ocorreu.


    def buscaVideo(self, idFilme:int=None, status:int=0):        

        comFilme = [] # Lista de vídeos que já transmitem o filme.
        for v in self.videos['comFilme']: 
            if v.filme != None:
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
        
        # Retorna as listas de vídeos que já transmitem o filme, 
        # que não transmitem o filme 
        # e que possuem um filme, mas não tem clientes assistindo.
        return comFilme, comStatus, comFilmeEStatus


    def pertoComVaga(self, cliente:OrqCliente, videos:list) -> OrqVideo:
        proximos = self.maisPerto(cliente, videos) # Retorna uma lista de vídeos ordenados por proximidade.
        for v in proximos:
            if v['video'].haVaga()[0]:
                return v
        return None
                
    def maisPerto(self, cliente:OrqCliente, videos:list):
        # Retorna uma lista de vídeos ordenados por proximidade.
        distancias = []
        for v in videos:
            distancias.append({'video': v, 'distancia': cliente.buscaDistancia(v.id)})
        distancias.sort(key=lambda x: x['distancia'])
        return distancias
    
    def selecionarCaso(self, cliente:OrqCliente, video:OrqVideo=None, distancia:float=None, caso:int=None, op:int=None):
        # Caso = 1: O video está transmitindo esse filme e há vagas
        # Caso = 2: Não há nenhum vídeo transmitindo o filme, mas ele é o mais proximo.

        while self.stream.blocked == True:
            print("\n ++++++ O ORQ ainda está recebendo este filme. Aguarde um momento. Por favor. \n")
            sleep(3)
        
        while video.recebendo == True:
            print("\n ****** O vídeo ainda está recebendo o filme. por favor aguarde ")
            sleep(1.2)

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



