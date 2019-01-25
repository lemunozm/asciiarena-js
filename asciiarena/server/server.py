from common.network_manager import NetworkManager
from common.logging import logger
from common import version
from .server_manager import ServerManager

class Server:
    def __init__(self, players, points, arena_size, seed):
        self._server_manager = ServerManager(players, points, arena_size, seed)

    def run(self, port):
        logger.info("Server version: {}".format(version.CURRENT))
        network = NetworkManager(self._server_manager)

        if network.listen(port):
            network.run()
            self._server_manager.process_requests()
            network.stop()

