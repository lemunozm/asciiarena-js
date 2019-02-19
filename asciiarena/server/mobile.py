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


    def _compute_movement(self):
        if self._has_movement:
            current = time.time()
            if current - self._last_movement_time_stamp > 1.0 / self._speed:
                self._last_movement_time_stamp = current
                movement = Direction.as_vector(self._direction)
                self._position += movement


    def check_collision(self, ground, collisionable_mobile_list):
        for mobile in collisionable_mobile_list:
            if mobile != self and mobile.get_position() == self._position:
                self.on_mobile_collision(mobile)
                return True

        if ground.is_blocked(self._position):
            self.on_wall_collision(self._position, ground.get_at(self._position))
            return True

        return False

    def update_movement(self, ground, collisionable_mobile_list):
        previous_position = self._position.copy()

        self._compute_movement()
        if self._position != previous_position:
            if self.check_collision(ground, collisionable_mobile_list):
                self._position = previous_position


    def on_mobile_collision(self, entity):
        pass


    def on_wall_collision(self, wall_position, terrain):
        pass

