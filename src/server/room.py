from enum import Enum

class Room:
    def __init__(self, max_participants):
        self._participant_dict = {}
        self._max_participants = max_participants
        self._open = True

    def add_participant(self, name, participant):
        if self.is_close():
            return False
        if self.is_complete():
            return False
        if self.has_participant(name):
            return False

        self._participant_dict[name] = participant
        return True

    def open(sefl, value):
        self._open = value

    def is_open(self):
        return self._open

    def is_complete(self, name, participant):
        return len(self._participant_dict) == self._max_participants

    def has_participant(self, name):
        self._participant_dict[name]

    def get_participant_dict(self):
        return self._participant_dict


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


class PlayerRoom(Room):
    def __init__(self, max_players, points_to_win):
        Room.__init__(self, max_players)
        self._points_to_win = points_to_win

    def add_player(self, character, socket):
        player = Player(character, socket)
        return Room.add_participant(self, character, player)

    def get_character_list(self):
        character_list = []
        for character in self.get_participant_dict():
            character_list.append(character)
        return character_list

    def get_winner_list(self):
        winner_list = []
        for player in self.get_participant_dict().values():
            if player.get_points() >= self._points_to_win:
                winner_list.append(player)
        return winner_list

    def get_socket_list(self):
        socket_list = []
        for player in self.get_participant_dict().values():
            socket_list.append(player.get_socket())
        return socket_list

    def get_points_to_win(self):
        return self._points_to_win
