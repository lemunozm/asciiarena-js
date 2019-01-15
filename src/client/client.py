from common import version, message

import socket
import string
import _pickle as pickle

class Client:
    def __init__(self, ip, port, character):
        self._ip = ip;
        self._port = port;
        self._character = character

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self._ip, self._port))

        if not self._check_version(sock):
            return

        if not self._check_game_info(sock):
            return

        if not self._login(sock):
            return

        print("Logged")

    def _check_version(self, sock):
        version_obj = message.Version(version.CURRENT)
        version_message = pickle.dumps(version_obj)
        sock.send(version_message)

        checked_version_message = sock.recv(message.MAX_BUFFER_SIZE)
        checked_version_obj = pickle.loads(checked_version_message)

        compatibility = "COMPATIBLE" if checked_version_obj.validation else "INCOMPATIBLE"
        print("Connected to server {}:{}".format(self._ip, self._port))
        print("Client version: {} - server version: {} - {}".format(version.CURRENT, checked_version_obj.value, compatibility))

        return compatibility

    def _check_game_info(self, sock):
        game_info_message = sock.recv(message.MAX_BUFFER_SIZE)
        game_info_obj = pickle.loads(game_info_message)

        player_list = game_info_obj.player_list
        max_players = game_info_obj.max_players
        points = game_info_obj.points
        map_size = game_info_obj.map_size
        seed_str = "random" if "" == game_info_obj.seed else game_info_obj.seed

        print("")
        print("Game: points to win: {} | map size: {} x {} | seed: {}".format(points, map_size, map_size, seed_str))
        print("      players: {} / {} - characters: {}".format(len(player_list), max_players, player_list))

        if len(player_list) == max_players:
            print("      The game is already started")
            return False

        return True

    def _login(self, sock):
        while True:
            if "" == self._character:
                self._character = Client._ask_character()
            status = self._login_request(sock)
            if message.PlayerLoginStatus.SUCCESFUL == status:
                return True
            if message.PlayerLoginStatus.GAME_COMPLETE == status:
                return False
            if message.PlayerLoginStatus.ALREADY_EXISTS == status:
                print("The character '" + serf._character + "' already exists.")
                self._character = ""

    def _login_request(self, sock):
        player_login_obj = message.PlayerLogin(self._character)
        player_login_message = pickle.dumps(player_login_obj)
        sock.send(player_login_message)

        player_login_status_message = sock.recv(message.MAX_BUFFER_SIZE)
        player_login_status_obj = pickle.loads(player_login_status_message)

        return player_login_status_obj.status

    @staticmethod
    def _ask_character():
        while True:
            character = input("      Choose a character (an unique letter from A to Z): ")
            if 1 == len(character) and -1 != string.ascii_uppercase.find(character):
                return character
