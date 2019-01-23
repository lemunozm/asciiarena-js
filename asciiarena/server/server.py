from common.network_communication import NetworkCommunication
from common.logging import logger
from common import version
from .server_manager import ServerManager

class Server:
    def __init__(self, max_players, points, map_size, seed):
        self._server_manager = ServerManager(max_players, points, map_size, seed)

    def run(self, port):
        logger.info("Server version: {}".format(version.CURRENT))
        network = NetworkCommunication(self._server_manager)

        if network.listen(port):
            network.run()
            self._server_manager.process_requests()
            network.stop()

