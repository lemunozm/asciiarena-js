from common.logging import logger
from common import version, message
from .message_queue import MessageQueue, ReceiveMessageError

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

        except ReceiveMessageError:
            print("Unexpected disconnection")

    def _server_info_request(self):
        version_message = message.Version(version.CURRENT)

        self._send_message(version_message)
        checked_version_message = self._receive_message()

        compatibility = "COMPATIBLE" if checked_version_message.validation else "INCOMPATIBLE"
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

        print("")
        print("Game: Points to win: {} | map size: {} x {} | seed: {}".format(self._points_to_win, self._map_size, self._map_size, printable_seed))
        print("      Players: {} / {} - characters: {}".format(len(self._character_list), self._max_players, self._character_list))
        return compatibility

    def _login_request(self):
        pass
"""
    def _login_request(self):
        while True:
            status = self._login(sock)
            if message.PlayerLoginStatus.GAME_CLOSED == status:
                return False
            if message.PlayerLoginStatus.ALREADY_EXISTS == status:
                continue
            if message.PlayerLoginStatus.SUCCESFUL == status:
                #wait()
                return True

    def _login(self, sock):
        if "" == self._character:
            self._character = Client._ask_user_for_character()

        player_login_message = message.PlayerLogin(self._character)
        self._send_message(player_login_message)
        communication.send(sock, player_login_message)

        player_login_status_message = communication.recv(sock)
        if message.PlayerLoginStatus.ALREADY_EXISTS == player_login_status_message.status:
            print("      Character '" + self._character + "' already exists.")
            self._character = ""

        return player_login_status_message.status

    @staticmethod
    def _ask_user_for_character():
        while True:
            character = input("      Choose a character (an unique letter from A to Z): ")
            if 1 == len(character) and -1 != string.ascii_uppercase.find(character):
                return character
"""
