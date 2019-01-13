import socket

class Server:
    def __init__(self, port):
        self._port = port
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.bind(('0.0.0.0', self.port))
        self._socket.listen()

    def run():
        while True:
            connection, address = self._socket.accept()
            data = connection.recv(4096)
            print(data)


