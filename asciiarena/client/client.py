from common.network_communication import NetworkCommunication
from common.logging import logger
from .client_manager import ClientManager
import socket

class Client:
    def __init__(self, character):
        self._client_manager = ClientManager(character)

    def run(self, ip, port):
        network = NetworkCommunication(self._client_manager)
        network.set_disconnection_callback(self._on_disconnect)

        server = network.connect(ip, port)
        if server:
            print("Connected to server {}:{}".format(ip, port))

            network.run()
            self._client_manager.init_communication(server)
            network.stop()

        else:
            print("Can not connect to server {}:{}".format(ip, port))

    def _on_disconnect(self, connection):
        server_ip, server_port = connection.getpeername()
        print("Disconnected from server {}:{}".format(server_ip, server_port))
