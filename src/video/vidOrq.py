import socket
from conector import Conector




class VidOrq(Conector):


    def __init__(
        self, 
        host: str = None, 
        port: int = None, 
        conn: socket = None, 
        addr: tuple = None
    ) -> None:
        super().__init__(host, port, conn, addr)