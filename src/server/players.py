from enum import Enum

class Player:
    def __init__(self, character, points, socket):
        self._character = character
        self._points = points
        self._socket = socket

    def get_character(self):
        return self._character

    def get_points(self):
        return self._points

    def get_socket(self):
        return self._socket

class PlayerRegistry:

    def __init__(self, max_players, points_to_win):
        self._player_list = []
        self._max_players = max_players
        self._points_to_win = points_to_win

    class Status(Enum):
        OK = 1
        ERROR_FULL = 2
        ERROR_ALREADY_EXISTS = 3

    def add_player(character):
        if is_complete():
            return ERROR_FULL
        if get_player():
            return ERROR_ALREADY_EXISTS

        new_player = Player(character, 0)
        player_list.add_player(new_player)
        return OK

    def is_complete():
        return len(self._player_list) == self._max_players

    def get_player(self, character):
        for player in player_list:
            if player.get_character() == character:
                return player
        return None

    def get_winners(self):
        winners = []
        for player in player_list:
            if player.get_points() >= points_to_win:
                winners.append(player)
        return winners

    def get_player_list(self):
        return self._player_list

    def get_max_players(self):
        return self._max_players

    def get_points_to_win(self):
        return self._points_to_win
