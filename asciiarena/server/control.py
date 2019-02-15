from .mobile import Mobile
from .entity import Entity
from .spell import Spell

from common.logging import logger
from common.direction import Direction
from common.util.vec2 import Vec2

import time

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


class Control():
    def update(self, state):
        pass


class MobileControl(Control):
    def __init__(self, mobile):
        self._controllable = mobile
        self._last_movement_time_stamp = 0


    def _compute_walking(self):
        if self._controllable.is_walking():
            current = time.time()
            if current - self._last_movement_time_stamp > 1.0 / self._controllable.get_speed():
                self._last_movement_time_stamp = current
                return Direction.as_vector(self._controllable.get_direction())

        return Vec2.zero()


    def update(self, state):
        super().update(state)

        movement = self._compute_walking()
        if movement != Vec2.zero():
            new_position = self._controllable.get_position() + movement
            if not state.get_ground().is_blocked(new_position) and not state.get_entity_at(new_position):
                self._controllable.set_position(new_position)


class EntityControl(MobileControl):
    def __init__(self, entity):
        MobileControl.__init__(self, entity)


    def update(self, state):
        super().update(state)


class SpellControl(MobileControl):
    def __init__(self, spell):
        MobileControl.__init__(self, spell)


    def update(self, state):
        super().update(state)


class PlayerControl(MobileControl):
    def __init__(self, entity):
        EntityControl.__init__(self, entity)
        self._last_cast_skill_action = None


    def move(self, direction):
        self._controllable.set_direction(direction)
        self._controllable.walk(True)
        if direction != self._controllable.get_direction():
            self._last_movement_time_stamp = 0


    def cast(self, skill):
        self._last_cast_skill_action = skill
        logger.debug("Player '{}' casts {}".format(self._controllable.get_character(), skill))


    def update(self, state):
        previous_position = self._controllable.get_position()

        super().update(state)
        self._controllable.walk(False)

        new_position = self._controllable.get_position()
        if previous_position != new_position:
            logger.debug("Player '{}' moves {}".format(self._controllable.get_character(), new_position - previous_position))


