class Version:
    def __init__(self, value):
        self.value = value


class CheckedVersion:
    def __init__(self, value, validation):
        self.value = value
        self.validation = validation


class GameInfo:
    def __init__(self, character_list, players, points, arena_size, seed, waiting_arena):
        self.character_list = character_list
        self.players = players
        self.points = points
        self.arena_size = arena_size
        self.seed = seed
        self.waiting_arena = waiting_arena


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


class ArenaInfo:
    def __init__(self, seed, ground):
        self.seed = seed
        self.ground = ground


class Frame:
    class Entity:
        def __init__(self, character, position):
            self.character = character
            self.position = position


    def __init__(self, entity_list):
        self.entity_list = entity_list


class PlayerMovement:
    def __init__(self, direction):
        self.direction = direction


class PlayerCast:
    def __init(self, skill_id):
        self.skill_id = skill_id


class PointsInfo:
    def __init__(self):
        pass

