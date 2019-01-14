from common import version, message

import socket
import threading
import _pickle as pickle

class GameConfig:
    def __init__(self, players, points):
        self.players = players
        self.points = points

class MapConfig:
    def __init__(self, map_size, seed):
        self.map_size = map_size
        self.seed = seed

class Server:
    def __init__(self, port, log_level, game_config, map_config):
        self._port = port
        self._game_config = game_config
        self._map_config = map_config
        self._log_level = log_level

    def run(self):
        server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_sock.bind(("0.0.0.0", self._port))
        server_sock.listen()

        while True:
            sock, address = server_sock.accept()
            thread = threading.Thread(target = self._client_connection, args = (sock,))
            thread.start()

    def _client_connection(self, sock):
        self._check_version(sock)
        self._check_game_info(sock)
        self._login(sock)

    def _check_version(self, sock):
        version_message = sock.recv(message.MAX_BUFFER_SIZE)
        version_obj = pickle.loads(version_message)

        validation = version.check(version_obj.value)

        checked_version_obj = message.CheckedVersion(version.CURRENT, validation)
        checked_version_message = pickle.dumps(checked_version_obj)
        sock.send(checked_version_message)

    def _check_game_info(self, sock):
        pass

    def _login(self, sock):
        pass
