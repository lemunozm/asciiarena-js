from .mobile import Mobile
from .entity import Entity
from .spell import Spell

from common.logging import logger
from common.direction import Direction
from common.util.vec2 import Vec2

class ArenaState:
    def __init__(self, step, ground, entity_list, spell_list):
        self._step = step
        self._ground = ground
        self._entity_list = entity_list
        self._spell_list = spell_list

    def get_step(self):
        return self._step


    def get_ground(self):
        return self._ground


    def get_entity_list(self):
        return self._entity_list


    def get_spell_list(self):
        return self._spell_list


    def get_entity_at(self, position):
        for entity in self._entity_list:
            if entity.get_position() == position:
                return entity

        return None


class EntityControl():
    def __init__(self, entity):
        self._entity = entity

    def update(self, state):
        raise NotImplementedError()


class PlayerControl(EntityControl):
    def __init__(self, entity):
        super().__init__(entity)
        self._last_step_position = entity.get_position()
        self._last_cast_skill = None


    def move(self, direction):
        self._entity.enable_movement(True)
        if direction != self._entity.get_direction():
            self._entity.set_direction(direction)
            self._entity.reset_movement_time_stamp()


    def cast(self, skill):
        self._last_cast_skill = skill


    def update(self, state):
        self._entity.enable_movement(False)
        last_movement = self._entity.get_position() - self._last_step_position
        if last_movement != Vec2.zero():
            self._last_step_position = self._entity.get_position()
            logger.debug("Player '{}' at step {} moves {}".format(self._entity.get_character(), state.get_step(), last_movement))

        if self._last_cast_skill != None:
            spell = self._entity.cast(self._last_cast_skill)
            if spell:
                logger.debug("Player '{}' at step {} casts {}".format(self._entity.get_character(), state.get_step(), self._last_cast_skill))
            self._last_cast_skill = None



