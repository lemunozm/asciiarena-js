from common.network_communication import NetworkCommunication
from common.logging import logger
from .client_manager import ClientManager

class Client:
    def __init__(self, character):
        self._client_manager = ClientManager()

    def run(self, ip, port):
        try:
            network = NetworkCommunication(self._client_manager)
            network.set_disconnection_callback(self._on_disconnect)
            server = network.connect(ip, port)
            logger.info("Connect to server on {}:{}".format(ip, port))

            network.run()

            self._client_manager.init_communication(server)

        except:
            logger.critical("Can not connect to the server {}:{}".format(ip, port))

    def _on_disconnect(self, connection):
        server_ip, server_port
        logger.debug("Connection lost with server {}:{}".format(server_ip, server_port))
        pass
