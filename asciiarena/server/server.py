from common.package_queue import PackageQueue
from common.network_communication import NetworkCommunication

class ServerManager(PackageQueue):
    def __init__(self):
        PackageQueue.__init__(self)

    def process_package(self):
        message, sender = self._input_queue.get()
        self._output_queue.put((message, sender))

class Server:
    def __init__(self, max_players, points, map_size, seed):
        self._server_manager = ServerManager()

    def run(self, port):
        network = NetworkCommunication(self._server_manager)
        network.listen(port)
        network.run()

        while True:
            self._server_manager.process_package()
