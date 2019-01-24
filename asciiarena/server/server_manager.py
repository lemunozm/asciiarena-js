from common.package_queue import PackageQueue, InputPack, OutputPack
from common.logging import logger
from common import version, message
from .room import PlayersRoom
from .match import Match

import threading
import time

class ServerManager(PackageQueue):
    def __init__(self, max_players, points, map_size, seed):
        PackageQueue.__init__(self)
        self._active = True
        self._room = PlayersRoom(max_players, points)
        self._game_thread = threading.Thread(target = self._run_game)
        self._game_thread.daemon = True
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
            else:
                self._lost_connection(input_pack.endpoint)

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

        if message.LoginStatus.LOGGED == status:
            players_info_message = message.PlayersInfo(self._room.get_character_list())
            self._output_queue.put(OutputPack(players_info_message, self._room.get_endpoint_list()))

            if self._room.is_complete():
                self._game_thread.start()

        elif message.LoginStatus.RECONNECTION == status:
            match_info_message = message.MatchInfo()
            self._output_queue.put(OutputPack(match_info_message, endpoint))

    def _register_player(self, character, endpoint):
        status = self._room.add_player(character, endpoint)

        if PlayersRoom.ADDITION_SUCCESSFUL == status:
            logger.info("Player '{}' registered successfully".format(character))
            return message.LoginStatus.LOGGED

        elif PlayersRoom.ADDITION_REUSE == status:
            logger.info("Player '{}' reconnected".format(character))
            return message.LoginStatus.RECONNECTION

        elif PlayersRoom.ADDITION_ERR_COMPLETE == status:
            logger.debug("Player '{}' tried to register: room complete".format(character))
            return message.LoginStatus.ROOM_COMPLETED

        elif PlayersRoom.ADDITION_ERR_ALREADY_EXISTS == status:
            logger.debug("Player '{}' tried to register: already exists".format(character))
            return message.LoginStatus.ALREADY_EXISTS

    def _lost_connection(self, endpoint):
        for player in self._room.get_participant_list():
            if player.get_endpoint() ==  endpoint:
                player.set_endpoint(None)
                logger.info("Player '{}' disconected".format(player.get_character()))
                return

    def _run_game(self):
        print("Start game!!")
        while [] == self._room.get_winner_list():
            match = Match()
            match_info_message = message.MatchInfo()
            self._output_queue.put(OutputPack(match_info_message, self._room.get_endpoint_list()))

            frame_count = 0
            while not match.has_finished():
                time.sleep(1)
                frame_message = message.Frame(frame_count)
                self._output_queue.put(OutputPack(frame_message, self._room.get_endpoint_list()))
                frame_count = frame_count + 1

