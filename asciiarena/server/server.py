from common.network_communication import NetworkCommunication
from common.logging import logger
from .server_manager import ServerManager

class Server:
    def __init__(self, max_players, points, map_size, seed):
        self._server_manager = ServerManager()

    def run(self, port):
        network = NetworkCommunication(self._server_manager)
        network.set_disconnection_callback(self._on_disconnect)

        if network.listen(port):
            network.run()

            while self._server_manager.is_active():
                self._server_manager.process_package()

            network.stop()

    def _on_disconnect(self, connection):
        #logout
        pass
