from common import version, message, communication
from .room import PlayerRoom
from .game_manager import GameManager

import socket
import logging
from threading import Thread, Lock
import _pickle as pickle

logger = logging.getLogger("asciiarena")

class Server:
    def __init__(self, port, max_players, points, map_size, seed):
        self._port = port
        self._player_room = PlayerRoom(max_players, points);
        self._game_manager = GameManager(self._player_room, map_size, seed)
        self._mutex = Lock()

    def run(self):
        try:
            server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_sock.bind(("0.0.0.0", self._port))
            server_sock.listen()

            logger.info("Server listening on port: {}".format(self._port))

            while True:
                sock, (client_ip, client_port) = server_sock.accept()
                logger.info("Connection request from {}:{}".format(client_ip, client_port))
                thread = Thread(target = self._client_connection, args = (sock,))
                thread.start()

        except OSError as error:
            logger.critical("Problem initializing the server, error: {}".format(error.errno))
            if(98 == error.errno):
                logger.critical("Port {} is already in use".format(self._port))

    def _client_connection(self, sock):
        try:
            client_message = communication.recv(sock)
            if message.Version == client_message.__class__:
                self._server_info_request(sock, client_message)

            elif message.PlayerLogin == client_message.__class__:
                with self._mutex:
                    if not self._login_request(sock, client_message):
                        return

                    if self._player_room.is_complete():
                        self._game_manager.init_game()

            else:
                (ip, port) = sock.getpeername()
                logger.warning("Rejected: unknown message received from {}:{}".format(ip, port))

        except communication.ConnectionLost:
            (ip, port) = sock.getpeername()
            logger.error("Connection lost with client {}:{}".format(ip, port))

        finally:
            sock.close()

    def _server_info_request(self, sock, version_message):
        if not self._check_version(sock, version_message):
            return

        character_list = self._player_room.get_character_list()
        max_players = self._player_room.get_max_participants()
        points = self._player_room.get_points_to_win()
        map_size = self._game_manager.get_map_size()
        seed = self._game_manager.get_seed()

        game_info_message = message.GameInfo(character_list, max_players, points, map_size, seed)
        communication.send(sock, game_info_message)

    def _check_version(self, sock, version_message):
        validation = version.check(version_message.value)

        if validation:
            logger.info("Client request with version {}".format(version_message.value))
        else:
            logger.warning("Client request with version {}: compatibility problems, rejected".format(version_message.value))

        checked_version_message = message.CheckedVersion(version.CURRENT, validation)
        communication.send(sock, checked_version_message)

        return validation

    def _login_request(self, sock, player_login_message):
        status = self._registry_player(sock, player_login_message.character)

        player_login_status_message = message.PlayerLoginStatus(status)
        communication.send(sock, player_login_status_message)

        if message.PlayerLoginStatus.SUCCESFUL == status:
            players_info_message = message.PlayersInfo(self._player_room.get_character_list())
            communication.sendAll(self._player_room.get_socket_list(), players_info_message)
            return True

        if message.PlayerLoginStatus.GAME_CLOSED == status:
            return False

    def _registry_player(self, sock, character):
        if self._player_room.add_player(character, sock):
            logger.info("Player registered '{}'".format(character))
            return message.PlayerLoginStatus.SUCCESFUL
        else:
            if self._player_room.is_complete() or not self._player_room.is_open():
                logger.info("Player registry try '{}': game full".format(character))
                return message.PlayerLoginStatus.GAME_CLOSED
            else:
                logger.info("Player registry try '{}': already exists".format(character))
                return message.PlayerLoginStatus.ALREADY_EXISTS

