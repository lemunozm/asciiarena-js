from .ground import Ground
from .entity import Entity

from common.direction import Direction
from common.util.vec2 import Vec2

class Arena:
    def __init__(self, dimension, seed, character_list):
        self._ground = Ground.fromSeed(dimension, seed)
        self._entity_list = []
        self._spell_list = []

        position_list = self._ground.find_separated_positions(len(character_list), 5) # TODO: check the minimum distance
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
            if entity.get_last_attempt_to_move() != Vec2.zero():
                expected_position = entity.get_position() + entity.get_last_attempt_to_move()
                if not self._ground.is_blocked(expected_position) and not self.entity_at(expected_position):
                    entity.set_position(expected_position)

        """
        # Check spells movements
        for spell in self._spell_list:
            if spell.get_last_attempt_to_move() != Vec2.zero():
                expected_position = spell.get_position() + spell.get_last_attempt_to_move()
                if not self._ground.is_blocked(expected_position) and not self.entity_at(expected_position):
                    spell.set_position(expected_position)

        # Check entity cast
        for entity in self._entity_list:
            spell = entity.get_last_attempt_to_cast()
            if spell:
                self._spell_list.append(spell)

        # Check spells actions
        for spell in self._spell_list:
            if True: #time event
                pass

            elif self._ground.is_blocked(spell.get_position()):
                spell.wall_collision()

            else:
                entity = self.entity_at(expected_position)
                if entity:
                    spell.entity_collision(entity)

        """
        # Clear entity last actions
        for entity in self._entity_list:
            entity.clear_last_attemps()

        """
        # Clear spell last actions
        for spell in self._spell_list:
            spell.clear_last_attemps()
        """
