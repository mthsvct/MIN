import socket

class OrqVideo:

    # Funções que envia e recebe sinais a um vídeo do orquestrador.
    
    id = 1

    def __init__(self, host:str='localhost', port:int=3000, x=0, y=0):
        self.id = OrqVideo.id
        self.host = host
        self.port = port
        self.socket = None
        self.x = x
        self.y = y
        OrqVideo.id += 1
    
    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            self.socket = s
            self.socket.connect((self.host, self.port)) # Conecta ao vídeo
            self.socket.sendall(f"{self.x};{self.y}".encode())
            dados = self.socket.recv(1024)
            print(dados.decode())




