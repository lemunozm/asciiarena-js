from common import version, message, communication
from .players import PlayerRegistry
from .game_manager import GameManager

import socket
import threading
import _pickle as pickle

class Server:
    def __init__(self, port, max_players, points, map_size, seed, log_level):
        self._port = port
        self._player_registry = PlayerRegistry(max_players, points);
        self._game_manager = GameManager(self._player_registry, map_size, seed)
        self._log_level = log_level

    def run(self):
        server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_sock.bind(("0.0.0.0", self._port))
        server_sock.listen()

        while True:
            sock, address = server_sock.accept()
            thread = threading.Thread(target = self._client_connection, args = (sock,))
            thread.start()

    def _client_connection(self, sock):
        if not self._check_version(sock):
            return

        if not self._check_game_info(sock):
            return

        if not self._login(sock):
            return

        if self._player_registry.is_complete():
            self._game_manager.init_game()

    def _check_version(self, sock):
        version_message = communication.recv(sock)

        validation = version.check(version_message.value)

        checked_version_message = message.CheckedVersion(version.CURRENT, validation)
        communication.send(sock, checked_version_message)

        return validation

    def _check_game_info(self, sock):
        character_list = self._player_registry.get_character_list()
        max_players = self._player_registry.get_max_players()
        points = self._player_registry.get_points_to_win()
        map_size = self._game_manager.get_map_size()
        seed = self._game_manager.get_seed()

        game_info_message = message.GameInfo(character_list, max_players, points, map_size, seed)
        communication.send(sock, game_info_message)

        return not self._player_registry.is_complete()

    def _login(self, sock):
        while True:
            player_login_message = communication.recv(sock)
            status = self._registry_player(sock, player_login_message.character)

            player_login_status_message = message.PlayerLoginStatus(status)
            communication.send(sock, player_login_status_message)

            if message.PlayerLoginStatus.SUCCESFUL == status:
                players_info_message = message.PlayersInfo(self._player_registry.get_character_list())
                communication.sendAll(self._player_registry.get_socket_list(), players_info_message)
                return True
            if message.PlayerLoginStatus.GAME_COMPLETE == status:
                return False

    def _registry_player(self, sock, character):
        if self._player_registry.add_player(character, sock):
            return message.PlayerLoginStatus.SUCCESFUL
        else:
            if self._player_registry.is_complete():
                return message.PlayerLoginStatus.GAME_COMPLETE
            else:
                return message.PlayerLoginStatus.ALREADY_EXISTS




