class ServerManager(PackageQueue):
    def __init__(self):
        pass

    def _process_package(self):
        message, sender = self._input_queue.get()
        self._output_queue.put((mesage, sender))

class Server:
    def __init__(self):
        self._server_manager = ServerManager()

    def run(self, port):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setblocking(False)
        server_socket.bind(('localhost', 10000))
        server_socket.listen()

        network = NetworkCommunication(self._server_manager)
        network.add_server_socket(server_socket)
        network.run()

        while True:
            self._server_manager.process_package()
