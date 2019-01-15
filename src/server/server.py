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
        if not self._check_version(sock):
            return

        if not self._check_game_info(sock):
            return

        if not self._login(sock):
            return

        print("Loggued")

    def _check_version(self, sock):
        version_message = sock.recv(message.MAX_BUFFER_SIZE)
        version_obj = pickle.loads(version_message)

        validation = version.check(version_obj.value)

        checked_version_obj = message.CheckedVersion(version.CURRENT, validation)
        checked_version_message = pickle.dumps(checked_version_obj)
        sock.send(checked_version_message)

        return validation

    def _check_game_info(self, sock):
        player_list = self._player_registry.get_character_list()
        max_players = self._player_registry.get_max_players()
        points = self._player_registry.get_points_to_win()
        map_size = self._game_manager.get_map_size()
        seed = self._game_manager.get_seed()

        game_info_obj = message.GameInfo(player_list, max_players, points, map_size, seed)
        game_info_message = pickle.dumps(game_info_obj)
        sock.send(game_info_message)

        return len(player_list) != max_players

    def _login(self, sock):
        while True:
            status = self._login_request(sock)
            if message.PlayerLoginStatus.SUCCESFUL == status:
                return True
            if message.PlayerLoginStatus.GAME_COMPLETE == status:
                return False

    def _login_request(self, sock):
        player_login_message = sock.recv(message.MAX_BUFFER_SIZE)
        player_login_obj = pickle.loads(player_login_message)

        status = self._registry_player(sock, player_login_obj.character)

        player_login_status_obj = message.PlayerLoginStatus(status)
        player_login_status_message = pickle.dumps(player_login_status_obj)
        sock.send(player_login_status_message)

        if message.PlayerLoginStatus.SUCCESFUL == status:
            #sendAll
            pass

        return status

    def _registry_player(self, sock, character):
        if self._player_registry.add_player(character, sock):
            return message.PlayerLoginStatus.SUCCESFUL
        else:
            if self._player_registry.is_complete():
                return message.PlayerLoginStatus.GAME_COMPLETE
            else:
                return message.PlayerLoginStatus.ALREADY_EXISTS




