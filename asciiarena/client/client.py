
class ClientManager(PackageQueue):
    def __init__(self):
        pass

    def init_communication(self, receiver):
        self._output_queue.put("First message", receiver)

class Client:
    def __init__(self):
        self._client_manager = ClientManager()

    def run(self, ip, port):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setblocking(False)
        server.connect((ip, port))

        network = NetworkCommunication(self._client_manager)
        network.add_connection(sock)
        network.run()

        self._client_manager.init_communication(server)
