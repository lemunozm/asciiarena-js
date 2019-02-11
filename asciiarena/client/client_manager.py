from .message_queue import MessageQueue, ReceiveMessageError
from .screen import TermScreen
from .game_scene import GameScene, GameSceneEvent

from common import version as Version, message as Message
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
        version_message = Message.Version(Version.CURRENT)

        self._send_message(version_message)
        checked_version_message = self._receive_message([Message.CheckedVersion])

        compatibility = "compatible" if checked_version_message.validation else "incompatible"
        print("Client version: {} - server version: {} - {}".format(Version.CURRENT, checked_version_message.value, compatibility))

        if not compatibility:
            self._end_communication()

        game_info_message = self._receive_message([Message.GameInfo])

        self._character_list = game_info_message.character_list
        self._players = game_info_message.players
        self._points_to_win = game_info_message.points
        self._arena_size = game_info_message.arena_size
        self._seed = game_info_message.seed
        printable_seed = "<random>" if "" == self._seed else self._seed

        print("\nGame: Points to win: {} | arena size: {} x {} | seed: {}".format(self._points_to_win, self._arena_size, self._arena_size, printable_seed))
        ClientManager._print_player_list(self._character_list, self._players)
        return compatibility


    def _login_request(self):
        while True:
            if "" == self._character:
                self._character = ClientManager._ask_user_for_character()

            login_message = Message.Login(self._character)
            self._send_message(login_message)

            login_status_message = self._receive_message([Message.LoginStatus])

            if Message.LoginStatus.ALREADY_EXISTS == login_status_message.status:
                print("      Character '" + self._character + "' already exists.")
                self._character = ""
                continue

            elif Message.LoginStatus.ROOM_COMPLETED == login_status_message.status:
                print("      Sorry, the game is already started. Try again later.")
                return False

            elif Message.LoginStatus.LOGGED == login_status_message.status:
                print("      Logged with character '" + self._character + "'.")
                return True

            elif Message.LoginStatus.RECONNECTION == login_status_message.status:
                print("      Reconnected with character '" + self._character + "'.")
                return True


    def _wait_game(self):
        while len(self._character_list) != self._players:
            player_info_message = self._receive_message([Message.PlayersInfo])
            self._character_list = player_info_message.character_list
            ClientManager._print_player_list(self._character_list, self._players)


    def _init_game(self):
        self._wait_to_start_game(0.20)
        arena_info_message = self._receive_message([Message.ArenaInfo])

        with TermScreen() as screen:
            game_scene = GameScene(screen, self._character, self._character_list, self._arena_size, arena_info_message.ground, arena_info_message.seed)

            while True:
                frame_message = self._receive_message([Message.Frame])

                event_list = game_scene.compute_events()

                for kind, event in event_list:
                    if kind == GameSceneEvent.PLAYER_MOVEMENT:
                        player_movement_message = Message.PlayerMovement(event)
                        self._send_message(player_movement_message)

                    elif kind == GameSceneEvent.PLAYER_CAST:
                        pass

                screen.clear()
                game_scene.render(frame_message.entity_list, [])
                screen.draw()


    def _wait_to_start_game(self, point_interval):
        print("Starting game", end = "", flush = True)

        last_point_time = 0
        while 0 == self._input_queue.qsize():
            current_time = time.time()
            if current_time - last_point_time > point_interval:
                print(".", end = "", flush = True)
                last_point_time = current_time

            time.sleep(0.001)

        print("")



    @staticmethod
    def _print_player_list(character_list, players):
        print("      Players: {} / {} - characters: {}".format(len(character_list), players, character_list))


    @staticmethod
    def _ask_user_for_character():
        while True:
            character = input("      Choose a character (an unique letter from A to Z): ")
            if 1 == len(character) and -1 != string.ascii_uppercase.find(character):
                return character

