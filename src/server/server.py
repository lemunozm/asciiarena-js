from common import version, message
from .players import PlayerRegistry
from .game_manager import GameManager

import socket
import threading
import _pickle as pickle

class Server:
    def __init__(self, port, max_players, points, map_size, seed, log_level):
        self._port = port
        self._player_registry = PlayerRegistry(max_players, points);
        self._game_manager = GameManager(map_size, seed)
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

        #Check here if all people are available

    def _check_version(self, sock):
        version_message = sock.recv(message.MAX_BUFFER_SIZE)
        version_obj = pickle.loads(version_message)

        validation = version.check(version_obj.value)

        checked_version_obj = message.CheckedVersion(version.CURRENT, validation)
        checked_version_message = pickle.dumps(checked_version_obj)
        sock.send(checked_version_message)

    def _check_game_info(self, sock):
        player_list = self._player_registry.get_player_list()
        max_players = self._player_registry.get_max_players()
        points = self._player_registry.get_points_to_win()
        map_size = self._game_manager.get_map_size()
        seed = self._game_manager.get_seed()

        game_info_obj = message.GameInfo(player_list, max_players, points, map_size, seed)
        game_info_message = pickle.dumps(game_info_obj)
        sock.send(game_info_message)

    def _login(self, sock):
        pass
