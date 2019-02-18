class Version:
    def __init__(self, value):
        self.value = value


class CheckedVersion:
    def __init__(self, value, validation):
        self.value = value
        self.validation = validation


class GameInfo:
    def __init__(self, character_list, players, points, arena_size, seed):
        self.character_list = character_list
        self.players = players
        self.points = points
        self.arena_size = arena_size
        self.seed = seed


class Login:
    def __init__(self, character):
        self.character = character


class LoginStatus:
    LOGGED = 1
    RECONNECTION = 2
    ROOM_COMPLETED = 3
    ALREADY_EXISTS = 4
    INVALID_CHARACTER = 5

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
        def __init__(self, character, position, direction):
            self.character = character
            self.position = position
            self.direction = direction

    class Spell:
        def __init__(self, spell_spec_class, position, direction):
            self.spell_spec_class = spell_spec_class
            self.position = position
            self.direction = direction

    def __init__(self, step, entity_list, spell_list):
        self.step = step
        self.entity_list = entity_list
        self.spell_list = spell_list


class PlayerMovement:
    def __init__(self, direction):
        self.direction = direction


class PlayerCast:
    def __init__(self, skill_id):
        self.skill_id = skill_id


class PointsInfo:
    def __init__(self):
        pass

