import socket
from threading import Thread
from time import sleep

from vidOrq import VidOrq
from vidFilme import VidFilme
from vidCliente import VidCliente
from conector import Conector

class Video(Conector):

    def __init__(
        self,
        host:str="localhost",
        port:int=4000 + int(input("Digite o digito final da porta (1, 2 e 3): ")),
        conn:socket.socket=None,
        addr:tuple=None,
        status:int=0, # 0 - Disponível, 1 - Ocupado
    ) -> None:
        self.x:int = None
        self.y:int = None
        self.orq:VidOrq = None
        self.status:int = status
        self.filme:VidFilme = None
        self.filmeEstaCompleto:bool = False
        self.clientes:list[VidCliente] = []
        self.limite:int = int(input("Digite o limite de clientes por vídeo: "))
        super().__init__(host, port, conn, addr)


    def run(self):
        try:
            self.rodarServ()
            self.escutar()
        except KeyboardInterrupt:
            print("\n----- 1 - Servidor encerrado -----\n")
        self.fechar()


    def escutar(self):
        while True:
            conn, addr = self.conn.accept()
            print(f"\n----- Conexão estabelecida - ({addr}) -----\n")
            nova = Thread(target=self.atendimento, args=(conn, addr,))
            nova.start()

    def atendimento(self, conn:socket.socket, addr:tuple):
        print(f"Atendimento do video.")

        # Primeiro recebe um sinal informando que tipo de cliente é
        # 1 - Orquestrador
        # 2 - Cliente

        aux = Conector(conn=conn, addr=addr)
        tipo = aux.receberLista()
        print(f"->>> Tipo: {tipo[0]} {tipo[0] == '2'}\n\n{tipo}")
        
        if tipo[0] == "1":
            # Orquestrador.
            # try:
            self.orq = VidOrq(conn=conn, addr=addr)
            self.orq.enviar(f"{self.limite}")
            self.atendimentoOrq()
            # except Exception as e:
                # print(f"Erro ao receber informações do orquestrador: {e}")
                # print("Erro ao receber informações do orquestrador")
                # conn.close()

        elif tipo[0] == "2":
            # Cliente que irá assistir o filme
            # try:
            idOrq = int(tipo[1])
            distancia = float(tipo[2])
            cliente = VidCliente(idOrq=idOrq, conn=conn, addr=addr, distancia=distancia)
            self.clientes.append(cliente)
            self.informarOrqEntrou(cliente)

            # while not self.filmeEstaCompleto:
            #     print("\n\nAguardando o filme ser recebido... Aguardando mais 5 segundos\n\n")
            #     sleep(5)

            self.atendimentoCli(cliente)
            # except Exception as e:
                # print(f"Erro ao receber informações do cliente: {e}, {e.args}")
                # print("Erro ao receber informações do cliente")
                # conn.close()

    
    def atendimentoOrq(self):
        while True:
            lSinal = self.orq.receberLista()
            sinal = int(lSinal[0])

            if sinal != 0:
                self.filmeEstaCompletoq = False
                self.filme = self.orq.receberFilme()
                self.filmeEstaCompleto = True
                print('\n' * 3)
                print(f"----Filme recebido: {self.filme}")
            else:
                print(f"Obrigado! {lSinal[1]}")
                break

    
    def atendimentoCli(self, cliente:VidCliente):
        cliente.transmitirFilme(self.filme) # Envia o filme para o cliente
        self.clientes.remove(cliente)       # Após a transmissão do filme, o cliente é removido da lista de clientes
        self.informarOrqSaiu(cliente)       # Informa ao orquestrador que o cliente saiu
        cliente.fechar()                    # Fecha a conexão com o cliente
        

    def informarOrqEntrou(self, cliente:VidCliente):
        self.atualizarStatus()
        # Opção indicando entrada de cliente, 
        # id do cliente e status do vídeo
        # status do video: 0 - Disponível, 1 - Ocupado
        # Quantidade de clientes no vídeo no momento
        # id do filme a ser transmitido
        print(f"{cliente.id};{self.status};{len(self.clientes)};{self.filme.id if self.filme != None else '-1'};")
        self.orq.enviar(f"{cliente.id};{self.status};{len(self.clientes)};{self.filme.id if self.filme != None else '-1'};")
    

    def informarOrqSaiu(self, cliente:VidCliente):
        self.atualizarStatus()
        # É enviado um sinal ao ORQ onde é informado o id do cliente que saiu, 
        # o novo status a após a saída do cliente 
        # E também a quantidade de clientes no vídeo no momento;
        self.orq.enviar(f"{cliente.id};{self.status};{len(self.clientes)};")


    def atualizarStatus(self):
        if len(self.clientes) == 0:
            self.status = 0
        else:
            self.status = 1



if __name__ == "__main__":
    video = Video()
    video.run()