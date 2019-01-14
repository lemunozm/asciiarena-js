from common import version, message

import socket
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

        seed_str = "random" if "" == game_info_obj.seed else game_info_obj.seed
        print("")
        print("Game: points to win: {} | map size: {} x {} | seed: {}".format(game_info_obj.points, game_info_obj.map_size, game_info_obj.map_size, seed_str))
        print("      players: {} / {} players - {}".format(len(game_info_obj.player_list), game_info_obj.max_players, game_info_obj.player_list))

        if len(game_info_obj.player_list) == game_info_obj.max_players:
            print("      The game is already started")
            return False

        return True

    def _login(self, sock):
        # Only returns if the game is full
        pass
