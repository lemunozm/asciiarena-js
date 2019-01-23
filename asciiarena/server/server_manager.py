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

        compatibility = "compatible" if validation else "incompatible"
        logger.debug("Server info request from client with version {} - {}".format(version_message.value, compatibility))

        character_list = self._room.get_character_list()
        max_players = self._room.get_max_participants()
        points = self._room.get_points_to_win()

        game_info_message = message.GameInfo(character_list, max_players, points, self._map_size, self._seed)
        self._output_queue.put(OutputPack(game_info_message, endpoint))

    def _login_request(self, login_message, endpoint):
        status = self._register_player(login_message.character, endpoint)

        login_status_message = message.LoginStatus(status)
        self._output_queue.put(OutputPack(login_status_message, endpoint))

        if message.LoginStatus.SUCCESFUL == status:
            players_info_message = message.PlayersInfo(self._room.get_character_list())
            self._output_queue.put(OutputPack(players_info_message, self._room.get_endpoint_list()))

            if self._room.is_complete():
                self._room.open(False)
                match_info_message = message.MatchInfo()
                self._output_queue.put(OutputPack(match_info_message, self._room.get_endpoint_list()))
                print("Start game!!")

    def _register_player(self, character, endpoint):
        if self._room.add_player(character, endpoint):
            logger.info("Player '{}' registered successfully".format(character))
            return message.LoginStatus.SUCCESFUL
        else:
            if not self._room.is_open() or self._room.is_complete():
                logger.debug("Player '{}' tried to register: room closed".format(character))
                return message.LoginStatus.ROOM_CLOSED
            else:
                logger.debug("Player '{}' tried to register: already exists".format(character))
                return message.LoginStatus.ALREADY_EXISTS

