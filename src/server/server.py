import socket
from time import sleep

class SStream:

    def __init__(self):
        self.port = 1234
        self.host = '127.0.0.1'
        self.filmes = [
            {'nome': 'Kill Bill', 'ano': 2003, 'genero': 'Ação', 'duracao': 69},
            {'nome': 'Sunset Boulevard', 'ano': 1950, 'genero': 'Drama', 'duracao': 110},
            {'nome': 'Onde os Fracos Não Têm Vez', 'ano': 2007, 'genero': 'Suspense', 'duracao': 97},
            {'nome': 'Bacurau', 'ano': 2019, 'genero': 'Suspense', 'duracao': 72},
            {'nome': 'The Graduate', 'ano': 1967, 'genero': 'Drama', 'duracao': 106},
        ]

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: # Cria um socket TCP/IP

            s.bind((self.host, self.port))

            while True:
                s.listen()
                print("Aguardando conexão...")
                conn, addr = s.accept()

                with conn:

                    print('Conectado com ', addr)
                    conn.sendall(self.menu().encode())
                    
                    op = conn.recv(1024)
                    op = int(op.decode() if op.decode() != '' else -1)

                    if op == -1:
                        print('Saindo...')
                        sleep(2)
                        conn.sendall('Saindo...'.encode())
                        conn.close()
                    
                    else:
                        print(f"Filme selecionado: {self.filmes[op]['nome']}") # Exibe o filme selecionado
                        sel = self.filmes[op]
                        cabecalho = f"\n{sel['nome']},{sel['ano']},{sel['genero']},{sel['duracao']};"
                        conn.sendall(cabecalho.encode())
                        

                        for i in range(sel['duracao']):
                            sleep(0.1)
                            mins = i // 60
                            secs = i % 60
                            conn.sendall(f'Minutagem Transmitida: {mins}:{secs}'.encode())
                            print(f'Enviando frame {i}...')
                        
                        conn.sendall('-1'.encode())

                print('Conexão encerrada.')


    def menu(self):
        m = 'Menu \n'
        for index, item in enumerate(self.filmes):
            m += f'{index} - {item["nome"]} ({item["ano"]})\n'
        m += f'{-1} - Sair\n'
        return m


if __name__ == '__main__':
    server = SStream()
    server.start()



