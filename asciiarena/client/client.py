from common.package_queue import PackageQueue
from common.network_communication import NetworkCommunication

class ClientManager(PackageQueue):
    def __init__(self):
        PackageQueue.__init__(self)

    def init_communication(self, receiver):
        self._output_queue.put(("First message", receiver))

class Client:
    def __init__(self, character):
        self._client_manager = ClientManager()

    def run(self, ip, port):
        network = NetworkCommunication(self._client_manager)
        server = network.connect(ip, port)
        network.run()

        self._client_manager.init_communication(server)
