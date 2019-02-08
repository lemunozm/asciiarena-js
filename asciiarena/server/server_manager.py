from common.package_queue import PackageQueue, InputPack, OutputPack
from common.logging import logger
from common import version, message
from .room import PlayersRoom
from .arena import Arena

import enum
import threading
import time
import string
import random

WAITING_TO_INIT_ARENA = 1.0 #seconds
FRAME_MAX_RATE = 60 #per second
RANDOM_SEED_SIZE = 6

class ServerSignal(enum.Enum):
    NEW_ARENA_SIGNAL = enum.auto()
    COMPUTE_FRAME_SIGNAL = enum.auto()


class ServerManager(PackageQueue):
    def __init__(self, players, points, arena_size, seed):
        PackageQueue.__init__(self)
        self._active = True
        self._room = PlayersRoom(players, points)
        self._arena_size = arena_size
        self._seed = seed
        self._arena = None
        self._last_frame_time_stamp = 0


    def process_requests(self):
        while self._active:
            input_pack = self._input_queue.get()
            if input_pack.message:
                if isinstance(input_pack.message, message.Version):
                    self._info_server_request(input_pack.message, input_pack.endpoint)

                elif isinstance(input_pack.message, message.Login):
                    self._login_request(input_pack.message, input_pack.endpoint)

                elif isinstance(input_pack.message, message.PlayerMovement):
                    self._player_movement_request(input_pack.message, input_pack.endpoint)

                elif isinstance(input_pack.message, message.PlayerCast):
                    self._player_cast_request(input_pack.message, input_pack.endpoint)

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
        logger.debug("Client with version {} - {}".format(version_message.value, compatibility))

        character_list = self._room.get_character_list()
        players = self._room.get_size()
        points = self._room.get_points_to_win()

        game_info_message = message.GameInfo(character_list, players, points, self._arena_size, self._seed, WAITING_TO_INIT_ARENA)
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


    def _player_movement_request(self, player_movement_message, endpoint):
        player = self._room.get_player_with_endpoint(endpoint)
        if 1 != player_movement_message.direction.get_length():
            logger.error("Unexpected movement value from player '{}'".format(player.get_character()))
            self._output_queue.put(OutputPack("", endpoint))
            return

        entity = self._get_entity_from_player(player)
        if entity:
            tried_to_move = entity.try_to_move(player_movement_message.direction)
            if tried_to_move:
                logger.debug("Player '{}' tried to move {}".format(entity.get_character(), player_movement_message.direction))


    def _player_cast_request(self, player_cast_message, endpoint):
        pass


    def _new_arena_signal(self):
        seed = self._seed if "" != self._seed else ServerManager.compute_random_seed(RANDOM_SEED_SIZE)
        logger.info("Start arena => size: {} - seed: {}".format(self._arena_size, seed))

        self._arena = Arena(self._arena_size, seed, self._room.get_character_list())

        arena_info_message = message.ArenaInfo(seed, self._arena.get_ground().get_grid())
        self._output_queue.put(OutputPack(arena_info_message, self._room.get_endpoint_list()))

        self._server_signal(ServerSignal.COMPUTE_FRAME_SIGNAL, WAITING_TO_INIT_ARENA)


    def _compute_frame_signal(self):
        self._arena.update()

        frame_entity_list = []
        for entity in self._arena.get_entity_list():
            frame_entity = message.Frame.Entity(entity.get_character(), entity.get_position())
            frame_entity_list.append(frame_entity)

        frame_message = message.Frame(frame_entity_list)
        self._output_queue.put(OutputPack(frame_message, self._room.get_endpoint_list()))

        if not self._arena.has_finished():
            current_time = time.time()
            last_frame_time = current_time - self._last_frame_time_stamp
            self._last_frame_time_stamp = current_time
            self._server_signal(ServerSignal.COMPUTE_FRAME_SIGNAL, 2 / FRAME_MAX_RATE - last_frame_time)

        elif [] == self._room.get_winner_list():
            self._server_signal(ServerSignal.NEW_ARENA_SIGNAL, 0)

        else:
            pass #TODO: reset signal => clear the room


    def _lost_connection(self, endpoint):
        player = self._room.get_player_with_endpoint(endpoint)
        if player:
            player.set_endpoint(None)
            logger.info("Player '{}' disconnected".format(player.get_character()))


    def _server_signal(self, signal, time):
        queue_signal = lambda: self._input_queue.put(InputPack(signal, None))
        if time > 0:
            timer = threading.Timer(time, queue_signal)
            timer.daemon = True
            timer.start()
        else:
            queue_signal()


    def _get_entity_from_player(self, player):
        if player:
            for entity in self._arena.get_entity_list():
                if player.get_character() == entity.get_character():
                    return entity
        return None

    @staticmethod
    def compute_random_seed(size):
        char_list = string.ascii_uppercase + string.digits
        random_char_list = random.choices(char_list, k = size)
        return "".join(random_char_list)

