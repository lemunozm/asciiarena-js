MAX_BUFFER_SIZE = 4096

class Version:
    def __init__(self, value):
        self.value = value

class CheckedVersion:
    def __init__(self, value, validation):
        self.value = value
        self.validation = validation

class GameInfo:
    def __init__(self, player_list, max_players, points, map_size, seed):
        self.player_list = player_list
        self.max_players = max_players
        self.points = points
        self.map_size = map_size
        self.seed = seed
