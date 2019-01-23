from common.logging import logger
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

            # init match here

        except ReceiveMessageError:
            print("Unexpected disconnection")

    def _server_info_request(self):
        version_message = message.Version(version.CURRENT)

        self._send_message(version_message)
        checked_version_message = self._receive_message()

        compatibility = "compatible" if checked_version_message.validation else "incompatible"
        print("Client version: {} - server version: {} - {}".format(version.CURRENT, checked_version_message.value, compatibility))

        if not compatibility:
            self._end_communication()

        game_info_message = self._receive_message()

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

            login_status_message = self._receive_message()

            if message.LoginStatus.ALREADY_EXISTS == login_status_message.status:
                print("      Character '" + self._character + "' already exists.")
                self._character = ""
                continue

            elif message.LoginStatus.ROOM_CLOSED == login_status_message.status:
                print("      Sorry, the game is already started. Try again later.")
                return False

            elif message.LoginStatus.SUCCESFUL == login_status_message.status:
                print("      Logged with character '" + self._character + "'.")
                return True

    def _wait_game(self):
        while True:
            server_message = self._receive_message()

            if message.PlayersInfo == server_message.__class__:
                self._character_list = server_message.character_list
                ClientManager._print_player_list(self._character_list, self._max_players)

            elif message.MatchInfo == server_message.__class__:
                print("Start game!!")
                return

    @staticmethod
    def _print_player_list(character_list, max_players):
        print("      Players: {} / {} - characters: {}".format(len(character_list), max_players, character_list))

    @staticmethod
    def _ask_user_for_character():
        while True:
            character = input("      Choose a character (an unique letter from A to Z): ")
            if 1 == len(character) and -1 != string.ascii_uppercase.find(character):
                return character
