from common.network_communication import NetworkCommunication
from common.logging import logger
from .client_manager import ClientManager

class Client:
    def __init__(self, character):
        self._client_manager = ClientManager(character)

    def run(self, ip, port):
        network = NetworkCommunication(self._client_manager)

        server = network.connect(ip, port)
        if server:
            print("Connected to server {}:{}".format(ip, port))

            network.run()
            self._client_manager.init_communication(server)
            network.stop()

        else:
            print("Can not connect to server {}:{}".format(ip, port))

