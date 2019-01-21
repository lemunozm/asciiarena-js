from common.network_communication import NetworkCommunication
from common.logging import logger
from .server_manager import ServerManager

class Server:
    def __init__(self, max_players, points, map_size, seed):
        self._server_manager = ServerManager()

    def run(self, port):
        try:
            network = NetworkCommunication(self._server_manager)
            network.set_disconnection_callback(self._on_disconnect)
            network.listen(port)

            logger.info("Listening on port: {}".format(port))
            network.run()

            while True:
                self._server_manager.process_package()

        except OSError as error:
            logger.critical("Problem initializing the server, error: {}".format(error.errno))
            if(98 == error.errno):
                logger.critical("Port {} is already in use".format(port))

        except KeyboardInterrupt:
            print("")
            pass

    def _on_disconnect(self, connection):
        #logout
        pass
