from common.logging import logger
from common.terrain import Terrain
from common import version, message
from .message_queue import MessageQueue, ReceiveMessageError

import string

class ClientManager(MessageQueue):
    def __init__(self, character):
        MessageQueue.__init__(self)
        self._character = character
        self._character_list = []
        self._max_players = 0
        self._points_to_win = 0
        self._map_size = 0
        self._seed = ""

    def init_communication(self, endpoint):
        self._attach_endpoint(endpoint)

        try:
            if not self._server_info_request():
                return

            if not self._login_request():
                return

            self._wait_game();

            self._init_game();

        except ReceiveMessageError:
            print("Unexpected disconnection")

    def _server_info_request(self):
        version_message = message.Version(version.CURRENT)

        self._send_message(version_message)
        checked_version_message = self._receive_message([message.CheckedVersion])

        compatibility = "compatible" if checked_version_message.validation else "incompatible"
        print("Client version: {} - server version: {} - {}".format(version.CURRENT, checked_version_message.value, compatibility))

        if not compatibility:
            self._end_communication()

        game_info_message = self._receive_message([message.GameInfo])

        self._character_list = game_info_message.character_list
        self._max_players = game_info_message.max_players
        self._points_to_win = game_info_message.points
        self._map_size = game_info_message.map_size
        self._seed = game_info_message.seed
        printable_seed = "<random>" if "" == self._seed else self._seed

        print("\nGame: Points to win: {} | map size: {} x {} | seed: {}".format(self._points_to_win, self._map_size, self._map_size, printable_seed))
        ClientManager._print_player_list(self._character_list, self._max_players)
        return compatibility

    def _login_request(self):
        while True:
            if "" == self._character:
                self._character = ClientManager._ask_user_for_character()

            login_message = message.Login(self._character)
            self._send_message(login_message)

            login_status_message = self._receive_message([message.LoginStatus])

            if message.LoginStatus.ALREADY_EXISTS == login_status_message.status:
                print("      Character '" + self._character + "' already exists.")
                self._character = ""
                continue

            elif message.LoginStatus.ROOM_COMPLETED == login_status_message.status:
                print("      Sorry, the game is already started. Try again later.")
                return False

            elif message.LoginStatus.LOGGED == login_status_message.status:
                print("      Logged with character '" + self._character + "'.")
                return True

            elif message.LoginStatus.RECONNECTION == login_status_message.status:
                print("      Reconnection with character '" + self._character + "'.")
                return True

    def _wait_game(self):
        while len(self._character_list) != self._max_players:
            player_info_message = self._receive_message([message.PlayersInfo])
            self._character_list = player_info_message.character_list
            ClientManager._print_player_list(self._character_list, self._max_players)

    def _init_game(self):
        match_info_message = self._receive_message([message.MatchInfo])
        ClientManager._print_ground(match_info_message.grid, self._map_size)
        while True:
            frame_message = self._receive_message([message.Frame])
            print("Frame stamp: {}".format(frame_message.stamp))

    @staticmethod
    def _print_ground(grid, dimension):
        ground = ""
        for i, terrain in enumerate(grid):
            if terrain == Terrain.EMPTY:
                ground += "  "
            elif terrain == Terrain.BORDER_WALL:
                ground += "X "
            elif terrain == Terrain.BLOCKED:
                ground += "· "
            else:
                ground += "? "
            if 0 == (i + 1) % dimension:
                ground += "\n"
        print(ground)

    @staticmethod
    def _print_player_list(character_list, max_players):
        print("      Players: {} / {} - characters: {}".format(len(character_list), max_players, character_list))

    @staticmethod
    def _ask_user_for_character():
        while True:
            character = input("      Choose a character (an unique letter from A to Z): ")
            if 1 == len(character) and -1 != string.ascii_uppercase.find(character):
                return character
