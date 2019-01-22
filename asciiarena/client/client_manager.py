from common.package_queue import PackageQueue, InputPack, OutputPack
from common.logging import logger
from common import version, message

class MessageQueue(PackageQueue):
    def __init__(self):
        PackageQueue.__init__(self)

    def _attach_endpoint(self, endpoint):
        self._endpoint = endpoint

    def _receive_message(self):
        return self._input_queue.get(timeout = 2).message

    def _send_message(self, message):
        self._output_queue.put(OutputPack(message, self._endpoint))

    def _end_communication(self):
        self._output_queue.put(OutputPack(None, self._endpoint))

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

        if not self._server_info_request():
            return

        if not self._login_request():
            return

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
        return False
