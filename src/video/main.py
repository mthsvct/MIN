import socket



class Video:

    id = 1

    def __init__(self, host="localhost", port=3001):
        self.id = Video.id
        self.host = host
        self.port = port
        self.socket = None
        self.x:int = None
        self.y:int = None
        Video.id += 1

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            self.socket = s
            self.socket.bind((self.host, self.port))
            self.socket.listen()

            print(f"Vídeo {self.id} escutando em {self.host}:{self.port}")

            try:
                while True:
                    conn, addr = self.socket.accept()
                    print(f"Conectado a {addr}")
                    dados = conn.recv(1024)
                    print(f"Dados recebidos do cliente: {dados.decode()}")
                    conn.sendall(b"Conectado ao video")

            except KeyboardInterrupt:
                print("\nEncerrando...")
                


if __name__ == "__main__":
    video = Video()
    video.run()
