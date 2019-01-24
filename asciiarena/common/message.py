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

class Login:
    def __init__(self, character):
        self.character = character

class LoginStatus:
    LOGGED = 1
    RECONNECTION = 2
    ROOM_COMPLETED = 3
    ALREADY_EXISTS = 4
    def __init__(self, status):
        self.status = status

class PlayersInfo:
    def __init__(self, character_list):
        self.character_list = character_list

class MatchInfo:
    def __init__(self, seed, grid):
        self.seed = seed
        self.grid = grid

class Frame:
    def __init__(self, stamp):
        self.stamp = stamp

class PlayerAction:
    class Movement:
        def __init__(self, direction):
            self.direction = direction

    class Shoot:
        def __init(self, skill_id):
            self.skill_id = skill_id

    def __init__(self, action):
        self.action = action
