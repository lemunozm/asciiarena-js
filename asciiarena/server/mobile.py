from common.direction import Direction
from common.util.vec2 import Vec2

import time

DEFAULT_SPEED = 8


class Mobile:
    def __init__(self, position):
        self._position = position
        self._direction = Direction.NONE
        self._speed = DEFAULT_SPEED
        self._has_movement = False
        self._last_movement_time_stamp = 0

    def get_position(self):
        return self._position


    def get_direction(self):
        return self._direction


    def get_direction_vec(self):
        return Direction.as_vector(self._direction)


    def get_speed(self):
        return self._speed


    def has_movement(self):
        return self._has_movement


    def set_direction(self, direction):
        self._direction = direction


    def set_position(self, position):
        self._position = position


    def displace(self, displacement):
        self._position += displacement


    def set_speed(self, speed):
        self._speed = speed


    def enable_movement(self, value):
        self._has_movement = value


    def reset_movement_time_stamp(self):
        self._last_movement_time_stamp = 0


    def compute_movement(self):
        if self._has_movement:
            current = time.time()

            if current - self._last_movement_time_stamp > 1.0 / self._speed:
                self._last_movement_time_stamp = current
                movement = Direction.as_vector(self._direction)
                self._position += movement

