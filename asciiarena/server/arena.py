from .ground import Ground
from .entity import Entity

from common.direction import Direction
from common.util.vec2 import Vec2

class Arena:
    def __init__(self, dimension, seed, character_list):
        self._ground = Ground.fromSeed(dimension, seed)
        self._entity_list = []

        position_list = self._ground.find_separated_positions(len(character_list), 5) #check the minimum distance
        for i, character in enumerate(character_list):
            entity = Entity(character, position_list[i])
            entity.set_direction(Direction.DOWN)
            self._entity_list.append(entity)


    def get_ground(self):
        return self._ground


    def get_entity_list(self):
        return self._entity_list


    def has_finished(self):
        return False


    def entity_at(self, position):
        for entity in self._entity_list:
            if entity.get_position() == position:
                return entity
        return None


    def update(self):
        # Check entity movements
        for entity in self._entity_list:
            if Vec2.zero() != entity.get_last_attempt_to_move():
                expected_position = entity.get_position() + entity.get_last_attempt_to_move()
                if not self._ground.is_blocked(expected_position) and not self.entity_at(expected_position):
                    entity.set_position(expected_position)

        # Clear last actions
        for entity in self._entity_list:
            entity.clear_last_attemps()
