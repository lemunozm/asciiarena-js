from enum import Enum

class Player:
    def __init__(self, character, endpoint):
        self._character = character
        self._endpoint = endpoint
        self._control = None
        self._points = 0


    def get_character(self):
        return self._character


    def set_endpoint(self, endpoint):
        self._endpoint = endpoint


    def get_endpoint(self):
        return self._endpoint


    def get_control(self):
        return self._control


    def set_control(self, control):
        self._control = control


    def get_points(self):
        return self._points


class Room:
    ADDITION_SUCCESSFUL = 1
    ADDITION_ERR_COMPLETE = 2
    ADDITION_ERR_ALREADY_EXISTS = 3
    ADDITION_REUSE = 4

    def __init__(self, size, points_to_win):
        self._player_dict = {}
        self._size = size
        self._points_to_win = points_to_win


    def add_player(self, character, endpoint):
        player = self.get_player(character)
        if player:
            if None == player.get_endpoint():
                player.set_endpoint(endpoint)
                return Room.ADDITION_REUSE

            else:
                return Room.ADDITION_ERR_ALREADY_EXISTS

        if self.is_complete():
            return Room.ADDITION_ERR_COMPLETE

        else:
            new_player = Player(character, endpoint)
            self._player_dict[character] = new_player
            return Room.ADDITION_SUCCESSFUL


    def is_complete(self):
        return len(self._player_dict) == self._size


    def get_player(self, character):
        return self._player_dict.get(character, None)


    def get_player_list(self):
        return self._player_dict.values()


    def get_size(self):
        return self._size


    def get_character_list(self):
        character_list = []
        for character in self._player_dict.keys():
            character_list.append(character)
        return character_list


    def get_winner_list(self):
        winner_list = []
        for player in self._player_dict.values():
            if player.get_points() >= self._points_to_win:
                winner_list.append(player)
        return winner_list


    def get_endpoint_list(self):
        endpoint_list = []
        for player in self._player_dict.values():
            if player.get_endpoint() != None:
                endpoint_list.append(player.get_endpoint())
        return endpoint_list


    def get_points_to_win(self):
        return self._points_to_win


    def get_player_with_endpoint(self, endpoint):
        for player in self._player_dict.values():
            if player.get_endpoint() == endpoint:
                return player
        return None


    def get_character_list_with_endpoints(self):
        character_list = []
        for player in self._player_dict.values():
            if player.get_endpoint() != None:
                character_list.append(player.get_character())

        return character_list
