from common.package_queue import PackageQueue, InputPack, OutputPack
from common.logging import logger
from common import version, message
from .room import PlayersRoom

class ServerManager(PackageQueue):
    def __init__(self, max_players, points, map_size, seed):
        PackageQueue.__init__(self)
        self._active = True
        self._room = PlayersRoom(max_players, points)
        self._map_size = map_size
        self._seed = seed

    def process_requests(self):
        while self._active:
            input_pack = self._input_queue.get()
            if "" != input_pack.message:
                if message.Version == input_pack.message.__class__:
                    self._info_server_request(input_pack.message, input_pack.endpoint)

                elif message.Login == input_pack.message.__class__:
                    self._login_request(input_pack.message, input_pack.endpoint)

                else:
                    logger.error("Unknown message type: {} - Rejecting connection...".format(input_pack.message.__class__));
                    self._output_queue(OutputPack(None, input_pack.endpoint))

    def _info_server_request(self, version_message, endpoint):
        validation = version.check(version_message.value)

        checked_version_message = message.CheckedVersion(version.CURRENT, validation)
        self._output_queue.put(OutputPack(checked_version_message, endpoint))

        compatibility = "COMPATIBLE" if validation else "INCOMPATIBLE"
        logger.info("Server info request from client with version {} - {}".format(version_message.value, compatibility))

        character_list = self._room.get_character_list()
        max_players = self._room.get_max_participants()
        points = self._room.get_points_to_win()

        game_info_message = message.GameInfo(character_list, max_players, points, self._map_size, self._seed)
        self._output_queue.put(OutputPack(game_info_message, endpoint))

    def _login_request(self, login_message, endpoint):
        pass

