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
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self._ip, self._port))

        if not self._check_version(sock):
            return

        if not self._check_game_info(sock):
            return

        if not self._login(sock):
            return

        self._wait_game(sock)
        print("init_game")

    def _check_version(self, sock):
        version_message = message.Version(version.CURRENT)
        communication.send(sock, version_message)

        checked_version_message = communication.recv(sock)

        compatibility = "COMPATIBLE" if checked_version_message.validation else "INCOMPATIBLE"
        print("Connected to server {}:{}".format(self._ip, self._port))
        print("Client version: {} - server version: {} - {}".format(version.CURRENT, checked_version_message.value, compatibility))

        return compatibility

    def _check_game_info(self, sock):
        game_info_message = communication.recv(sock)

        character_list = game_info_message.character_list
        self._max_players = game_info_message.max_players
        self._points_to_win = game_info_message.points
        self._map_size = game_info_message.map_size
        self._seed = game_info_message.seed
        printable_seed = "random" if "" == self._seed else self._seed

        print("")
        print("Game: points to win: {} | map size: {} x {} | seed: {}".format(self._points_to_win, self._map_size, self._map_size, printable_seed))
        print("      players: {} / {} - characters: {}".format(len(character_list), self._max_players, character_list))

        if len(character_list) == self._max_players:
            print("      the game is already started. Please, try later.")
            return False

        return True

    def _login(self, sock):
        while True:
            if "" == self._character:
                self._character = Client._ask_character()

            player_login_message = message.PlayerLogin(self._character)
            communication.send(sock, player_login_message)

            player_login_status_message = communication.recv(sock)
            if message.PlayerLoginStatus.SUCCESFUL == player_login_status_message.status:
                return True
            if message.PlayerLoginStatus.GAME_COMPLETE == player_login_status_message.status:
                return False
            if message.PlayerLoginStatus.ALREADY_EXISTS == player_login_status_message.status:
                print("      the character '" + serf._character + "' already exists.")
                self._character = ""

    def _wait_game(self, sock):
        while True:
            players_info_message = communication.recv(sock)

            character_list = players_info_message.character_list
            print("      players: {} / {} - characters: {}".format(len(character_list), self._max_players, character_list))

            if len(character_list) == self._max_players:
                return

    @staticmethod
    def _ask_character():
        while True:
            character = input("      choose a character (an unique letter from A to Z): ")
            if 1 == len(character) and -1 != string.ascii_uppercase.find(character):
                return character
