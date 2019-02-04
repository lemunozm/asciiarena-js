from enum import Enum

class Room:
    ADDITION_SUCCESSFUL = 1
    ADDITION_ERR_COMPLETE = 2
    ADDITION_ERR_ALREADY_EXISTS = 3

    def __init__(self, size):
        self._participant_dict = {}
        self._size = size


    def add_participant(self, name, participant):
        if self.is_complete():
            return Room.ADDITION_ERR_COMPLETE
        if self.get_participant(name):
            return Room.ADDITION_ERR_ALREADY_EXISTS

        self._participant_dict[name] = participant
        return Room.ADDITION_SUCCESSFUL


    def is_complete(self):
        return len(self._participant_dict) == self._size


    def get_participant(self, name):
        return self._participant_dict.get(name, None)


    def get_participant_list(self):
        return self._participant_dict.values()


    def get_size(self):
        return self._size


class Player:
    def __init__(self, character, endpoint):
        self._character = character
        self._endpoint = endpoint
        self._points = 0


    def get_character(self):
        return self._character


    def get_points(self):
        return self._points


    def set_endpoint(self, endpoint):
        self._endpoint = endpoint


    def get_endpoint(self):
        return self._endpoint


class PlayersRoom(Room):
    ADDITION_REUSE = 4
    def __init__(self, size, points_to_win):
        Room.__init__(self, size)
        self._points_to_win = points_to_win


    def add_player(self, character, endpoint):
        player = self.get_participant(character)
        if player and None == player.get_endpoint():
                player.set_endpoint(endpoint)
                return PlayersRoom.ADDITION_REUSE
        else:
            new_player = Player(character, endpoint)
            return self.add_participant(character, new_player)


    def get_character_list(self):
        character_list = []
        for character in self._participant_dict.keys():
            character_list.append(character)
        return character_list


    def get_winner_list(self):
        winner_list = []
        for player in self._participant_dict.values():
            if player.get_points() >= self._points_to_win:
                winner_list.append(player)
        return winner_list


    def get_endpoint_list(self):
        endpoint_list = []
        for player in self._participant_dict.values():
            if None != player.get_endpoint():
                endpoint_list.append(player.get_endpoint())
        return endpoint_list


    def get_points_to_win(self):
        return self._points_to_win


    def get_player_with_endpoint(self, endpoint):
        for player in self._participant_dict.values():
            if player.get_endpoint() == endpoint:
                return player
        return None

