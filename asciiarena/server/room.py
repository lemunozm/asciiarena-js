from enum import Enum

class Room:
    def __init__(self, max_participants):
        self._participant_dict = {}
        self._max_participants = max_participants
        self._open = True

    def add_participant(self, name, participant):
        if not self.is_open():
            return False
        if self.is_complete():
            return False
        if self.has_participant(name):
            return False

        self._participant_dict[name] = participant
        return True

    def open(self, value):
        self._open = value

    def is_open(self):
        return self._open

    def is_complete(self):
        return len(self._participant_dict) == self._max_participants

    def has_participant(self, name):
        return self._participant_dict.get(name, None)

    def get_participant_dict(self):
        return self._participant_dict

    def get_max_participants(self):
        return self._max_participants


class Player:
    def __init__(self, character, endpoint):
        self._character = character
        self._endpoint = endpoint
        self._points = 0

    def get_character(self):
        return self._character

    def get_points(self):
        return self._points

    def get_endpoint(self):
        return self._endpoint


class PlayersRoom(Room):
    def __init__(self, max_players, points_to_win):
        Room.__init__(self, max_players)
        self._points_to_win = points_to_win

    def add_player(self, character, endpoint):
        player = Player(character, endpoint)
        return Room.add_participant(self, character, player)

    def get_character_list(self):
        character_list = []
        for character in self.get_participant_dict().keys():
            character_list.append(character)
        return character_list

    def get_winner_list(self):
        winner_list = []
        for player in self.get_participant_dict().values():
            if player.get_points() >= self._points_to_win:
                winner_list.append(player)
        return winner_list

    def get_endpoint_list(self):
        endpoint_list = []
        for player in self.get_participant_dict().values():
            endpoint_list.append(player.get_endpoint())
        return endpoint_list

    def get_points_to_win(self):
        return self._points_to_win
