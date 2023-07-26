import socket

class Cliente:

    def __init__(self, filme:str='Kill Bill'):
        self.port = 1234
        self.host = '127.0.0.1'
        self.filme = filme # Filme que o cliente deseja assistir.

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: # Cria um socket TCP/IP
            s.connect((self.host, self.port))
            # s.sendall(self.filme.encode())

            c = 1
            while c < 2:
                menu = s.recv(1024) # Recebe os dados do servidor
                print(menu.decode()) # Recebe menu.
                op = input('Digite a opção desejada: ')
                s.sendall(op.encode())

                filme = s.recv(1024)
                print(filme.decode())

                duracao = int(filme.decode().split(';')[0].split(',')[3])

                while True:
                    frame = s.recv(1024)
                    if not frame: 
                        break
                    if frame.decode() == '-1': 
                        break
                    print(f"Frame recebido: {frame.decode()} / {duracao}")

                c += 1





if __name__ == '__main__':
    cliente = Cliente()
    cliente.start()
