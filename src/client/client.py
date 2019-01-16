from common import version, message, communication

import socket
import string
import _pickle as pickle

class Client:
    def __init__(self, ip, port, character):
        self._ip = ip;
        self._port = port;
        self._character = character
        self._max_players = 0
        self._points_to_win = 0
        self._map_size = 0
        self._seed = ""

    def run(self):
            if not self._server_info_request():
                return

            self._game_request()

    def _server_info_request(self):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((self._ip, self._port))

            if not self._check_version(sock):
                return False

            self._game_info(sock);
            return True

        except OSError:
            print("Error: can not connect to server {}:{}".format(self._ip, self._port))
        except communication.ConnectionLost:
            print("Error: connection lost with the server {}:{}".format(self._ip, self._port))
        finally:
            sock.close()

    def _check_version(self, sock):
        version_message = message.Version(version.CURRENT)
        communication.send(sock, version_message)

        checked_version_message = communication.recv(sock)

        compatibility = "COMPATIBLE" if checked_version_message.validation else "INCOMPATIBLE"
        print("Connected to server {}:{}".format(self._ip, self._port))
        print("Client version: {} - server version: {} - {}".format(version.CURRENT, checked_version_message.value, compatibility))
        print("")

        return compatibility

    def _game_info(self, sock):
        game_info_message = communication.recv(sock)

        character_list = game_info_message.character_list
        self._max_players = game_info_message.max_players
        self._points_to_win = game_info_message.points
        self._map_size = game_info_message.map_size
        self._seed = game_info_message.seed
        printable_seed = "random" if "" == self._seed else self._seed

        print("Game: Points to win: {} | map size: {} x {} | seed: {}".format(self._points_to_win, self._map_size, self._map_size, printable_seed))
        print("      Players: {} / {} - characters: {}".format(len(character_list), self._max_players, character_list))

    def _game_request(self):
        while True:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((self._ip, self._port))

                status = self._login(sock)
                if message.PlayerLoginStatus.GAME_CLOSED == status:
                    return False
                if message.PlayerLoginStatus.ALREADY_EXISTS == status:
                    continue
                if message.PlayerLoginStatus.SUCCESFUL == status:
                    self._wait_game(sock)
                    print("init_game")

            except OSError:
                print("Error: can not connect to server {}:{}".format(self._ip, self._port))
            except communication.ConnectionError:
                print("Error: connection lost with the server {}:{}".format(self._ip, self._port))
            finally:
                sock.close()

    def _login(self, sock):
        if "" == self._character:
            self._character = Client._ask_user_for_character()

        player_login_message = message.PlayerLogin(self._character)
        communication.send(sock, player_login_message)

        player_login_status_message = communication.recv(sock)
        if message.PlayerLoginStatus.ALREADY_EXISTS == player_login_status_message.status:
            print("      Character '" + self._character + "' already exists.")
            self._character = ""

        return player_login_status_message.status

    def _wait_game(self, sock):
        while True:
            server_message = communication.recv(sock)

            if message.PlayersInfo == server_message.__class__:
                character_list = players_info_message.character_list
                print("      Players: {} / {} - characters: {}".format(len(character_list), self._max_players, character_list))

            if message.GameInfo == server_message.__class__:
                return

    @staticmethod
    def _ask_user_for_character():
        while True:
            character = input("      Choose a character (an unique letter from A to Z): ")
            if 1 == len(character) and -1 != string.ascii_uppercase.find(character):
                return character
