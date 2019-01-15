MAX_BUFFER_SIZE = 4096

class Version:
    def __init__(self, value):
        self.value = value

class CheckedVersion:
    def __init__(self, value, validation):
        self.value = value
        self.validation = validation

class GameInfo:
    def __init__(self, character_list, max_players, points, map_size, seed):
        self.character_list = character_list
        self.max_players = max_players
        self.points = points
        self.map_size = map_size
        self.seed = seed

class PlayerLogin:
    def __init__(self, character):
        self.character = character

class PlayerLoginStatus:
    SUCCESFUL = 1
    ALREADY_EXISTS = 2
    GAME_COMPLETE = 3
    def __init__(self, status):
        self.status = status

class PlayersInfo:
    def __init__(self, character_list):
        self.character_list = character_list
