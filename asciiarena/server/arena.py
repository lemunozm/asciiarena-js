from .ground import Ground

class Entity:
    def __init__(self, character, position):
        self._character = character
        self._position = position

    def get_character(self):
        return self._character

    def get_position(self):
        return self._position

class Arena:
    def __init__(self, size, seed, character_list):
        self._ground = Ground.fromSeed(size, seed)
        self._entity_list = []

        position_list = self._ground.find_separated_positions(len(character_list), 5) #check the minimum distance
        for i, character in enumerate(character_list):
            entity = Entity(character, position_list[i])
            self._entity_list.append(entity)

    def character_moves(self, character, direction):
        pass

    def character_shoots(self, character, skill_id):
        pass

    def get_ground(self):
        return self._ground

    def get_entity_list(self):
        return self._entity_list

    def has_finished(self):
        return False

    def update(self):
        pass
