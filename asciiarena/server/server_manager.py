from common.package_queue import PackageQueue, InputPack, OutputPack
from common.logging import logger
from common import version, message
from .room import PlayersRoom
from .arena import Arena

from enum import Enum
import threading

class ServerSignal(Enum):
    NEW_ARENA_SIGNAL = 1
    COMPUTE_FRAME_SIGNAL = 2

class ServerManager(PackageQueue):
    def __init__(self, players, points, arena_size, seed):
        PackageQueue.__init__(self)
        self._active = True
        self._room = PlayersRoom(players, points)
        self._arena_size = arena_size
        self._seed = seed
        self._arena = None
        self._frame_stamp = 0

    def process_requests(self):
        while self._active:
            input_pack = self._input_queue.get()
            if input_pack.message:
                if isinstance(input_pack.message, message.Version):
                    self._info_server_request(input_pack.message, input_pack.endpoint)

                elif isinstance(input_pack.message, message.Login):
                    self._login_request(input_pack.message, input_pack.endpoint)

                elif isinstance(input_pack.message, message.PlayerAction):
                    self._player_action_request(input_pack.message, input_pack.endpoint)

                elif isinstance(input_pack.message, ServerSignal):
                    if ServerSignal.NEW_ARENA_SIGNAL == input_pack.message:
                        self._new_arena_signal()

                    elif ServerSignal.COMPUTE_FRAME_SIGNAL == input_pack.message:
                        self._compute_frame_signal()

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
        players = self._room.get_size()
        points = self._room.get_points_to_win()

        game_info_message = message.GameInfo(character_list, players, points, self._arena_size, self._seed)
        self._output_queue.put(OutputPack(game_info_message, endpoint))

    def _login_request(self, login_message, endpoint):
        status = self._register_player(login_message.character, endpoint)

        login_status_message = message.LoginStatus(status)
        self._output_queue.put(OutputPack(login_status_message, endpoint))

        if message.LoginStatus.LOGGED == status:
            players_info_message = message.PlayersInfo(self._room.get_character_list())
            self._output_queue.put(OutputPack(players_info_message, self._room.get_endpoint_list()))

            if self._room.is_complete():
                self._input_queue.put(InputPack(ServerSignal.NEW_ARENA_SIGNAL, None))

        elif message.LoginStatus.RECONNECTION == status:
            players_info_message = message.PlayersInfo(self._room.get_character_list())
            self._output_queue.put(OutputPack(players_info_message, endpoint))

            if self._arena:
                arena_info_message = message.ArenaInfo(self._arena.get_ground().get_seed(), self._arena.get_ground().get_grid())
                self._output_queue.put(OutputPack(arena_info_message, endpoint))

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

    def _player_action_request(self, player_action_message, endpoint):
        player = self._room.get_player_with_endpoint(endpoint)
        if player:
            if isinstance(player_action_message, message.PlayerAction.Movement):
                self._arena.character_moves(player.get_character(), player_action_message.action.movement)

            elif isinstance(player_action_message, message.PlayerAction.Shoot):
                self._arena.character_shoots(player.get_character(), player_action_message.action.skill_id)

            else:
                logger.error("Unknown player action type: {} - Rejecting connection...".format(player_action_message.action.__class__));
                self._output_queue(OutputPack(None, endpoint))

    def _new_arena_signal(self):
        print("Start arena!!")
        self._arena = Arena(self._arena_size, self._seed)
        self._frame_stamp = 0

        arena_info_message = message.ArenaInfo(self._arena.get_ground().get_seed(), self._arena.get_ground().get_grid())
        self._output_queue.put(OutputPack(arena_info_message, self._room.get_endpoint_list()))

        if not self._arena.has_finished():
            self._input_queue.put(InputPack(ServerSignal.COMPUTE_FRAME_SIGNAL, None))

        elif [] == self._room.get_winner_list():
            self._input_queue.put(InputPack(ServerSignal.NEW_ARENA_SIGNAL, None))

        else:
            pass #reset signal => clear the room


    def _compute_frame_signal(self):
        def enqueue_new_frame():
            self._input_queue.put(InputPack(ServerSignal.COMPUTE_FRAME_SIGNAL, None))

        frame_message = message.Frame(self._frame_stamp)
        self._output_queue.put(OutputPack(frame_message, self._room.get_endpoint_list()))

        self._frame_stamp = self._frame_stamp + 1

        timer = threading.Timer(1, enqueue_new_frame)
        timer.daemon = True
        timer.start()

    def _lost_connection(self, endpoint):
        player = self._room.get_player_with_endpoint(endpoint)
        if player:
            player.set_endpoint(None)
            logger.info("Player '{}' disconected".format(player.get_character()))

