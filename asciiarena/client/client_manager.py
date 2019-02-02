from .message_queue import MessageQueue, ReceiveMessageError
from .screen import TermScreen
from .game_window import GameWindow
from .keyboard import Keyboard, Key
from common.logging import logger
from common import version, message
from common.util.vec2 import Vec2

import string
import time

class ClientManager(MessageQueue):
    def __init__(self, character):
        MessageQueue.__init__(self)
        self._character = character
        self._character_list = []
        self._players = 0
        self._points_to_win = 0
        self._arena_size = 0
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
        self._players = game_info_message.players
        self._points_to_win = game_info_message.points
        self._arena_size = game_info_message.arena_size
        self._seed = game_info_message.seed
        self._waiting_time_to_arena = game_info_message.waiting_arena
        printable_seed = "<random>" if "" == self._seed else self._seed

        print("\nGame: Points to win: {} | arena size: {} x {} | seed: {}".format(self._points_to_win, self._arena_size, self._arena_size, printable_seed))
        ClientManager._print_player_list(self._character_list, self._players)
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
                print("      Reconnected with character '" + self._character + "'.")
                if len(self._character_list) == self._players:
                    self._waiting_time_to_arena = 0
                return True


    def _wait_game(self):
        while len(self._character_list) != self._players:
            player_info_message = self._receive_message([message.PlayersInfo])
            self._character_list = player_info_message.character_list
            ClientManager._print_player_list(self._character_list, self._players)


    def _init_game(self):
        ClientManager._print_starting_game(self._waiting_time_to_arena, 5)

        with TermScreen() as screen:
            keyboard = Keyboard()
            arena_info_message = self._receive_message([message.ArenaInfo])
            game_window = GameWindow(screen, self._arena_size, arena_info_message.ground, self._seed, self._character_list)

            while True:
                frame_message = self._receive_message([message.Frame])
                game_window.update(frame_message.entity_list, [])
                keyboard.update_key_events(screen.get_event_list())

                direction = self._ask_player_movement_direction(keyboard)
                if Vec2(0, 0) != direction:
                    player_movement_message = message.PlayerMovement(direction)
                    self._send_message(player_movement_message)


    @staticmethod
    def _ask_player_movement_direction(keyboard):
        if keyboard.is_key_down(Key.W):
            return Vec2(0, -1)
        elif keyboard.is_key_down(Key.A):
            return Vec2(-1, 0)
        elif keyboard.is_key_down(Key.S):
            return Vec2(0, 1)
        elif keyboard.is_key_down(Key.D):
            return Vec2(1, 0)
        else:
            return Vec2(0, 0)


    @staticmethod
    def _print_player_list(character_list, players):
        print("      Players: {} / {} - characters: {}".format(len(character_list), players, character_list))


    @staticmethod
    def _ask_user_for_character():
        while True:
            character = input("      Choose a character (an unique letter from A to Z): ")
            if 1 == len(character) and -1 != string.ascii_uppercase.find(character):
                return character


    @staticmethod
    def _print_starting_game(waiting_time, interval):
        print("Starting game ", end = "", flush = True)
        for i in range(0, interval):
            print(".", end = "", flush = True)
            time.sleep(waiting_time / interval)

        print("")

