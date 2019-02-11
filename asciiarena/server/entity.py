from common.direction import Direction
from common.util.vec2 import Vec2

import time

class Entity:
    def __init__(self, character, position):
        self._character = character
        self._position = position
        self._direction = Direction.NONE
        self._speed = 8

        self._last_move_attempt_time_stamp = 0
        self._last_attempt_to_move = Vec2.zero()
        self._last_attempt_to_cast = None


    def get_character(self):
        return self._character


    def get_position(self):
        return self._position


    def get_direction(self):
        return self._direction


    def set_direction(self, direction):
        self._direction = direction


    def get_last_attempt_to_move(self):
        return self._last_attempt_to_move


    def set_position(self, position):
        self._position = position


    def move(self, displacement):
        self._position += displacement


    def try_to_move(self, direction):
        current = time.time()
        if self._direction != direction:
            self._direction = direction
            self._last_attempt_to_move = Direction.as_vector(self._direction)
            self._last_move_attempt_time_stamp = current

        elif current - self._last_move_attempt_time_stamp > 1.0 / self._speed:
            self._last_attempt_to_move = Direction.as_vector(self._direction)
            self._last_move_attempt_time_stamp = current

        return current == self._last_move_attempt_time_stamp

    def try_to_cast(self, skill_spec):
        pass

    def clear_last_attemps(self):
        self._last_attempt_to_move = Vec2.zero()
        self._last_attempt_to_cast = None

