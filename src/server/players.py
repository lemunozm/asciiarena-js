from enum import Enum

class Player:
    def __init__(self, character, socket):
        self._character = character
        self._socket = socket
        self._points = 0

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

    def add_player(self, character, socket):
        if self.is_complete():
            return False
        if self.get_player(character):
            return False

        new_player = Player(character, socket)
        self._player_list.append(new_player)
        return True

    def is_complete(self):
        return len(self._player_list) == self._max_players

    def get_player(self, character):
        for player in self._player_list:
            if player.get_character() == character:
                return player
        return None

    def get_character_list(self):
        characters = []
        for player in self._player_list:
            characters.append(player.get_character())
        return characters

    def get_winner_list(self):
        winners = []
        for player in self._player_list:
            if player.get_points() >= self._points_to_win:
                winners.append(player)
        return winners

    def get_socket_list(self):
        sockets = []
        for player in self._player_list:
            sockets.append(player.get_socket())
        return sockets

    def get_player_list(self):
        return self._player_list

    def get_max_players(self):
        return self._max_players

    def get_points_to_win(self):
        return self._points_to_win
