from common.direction import Direction

DEFAULT_SPEED = 8

class Mobile:
    def __init__(self, position):
        self._control = None
        self._position = position
        self._direction = Direction.NONE
        self._speed = DEFAULT_SPEED
        self._moving = False

    def get_position(self):
        return self._position


    def get_direction(self):
        return self._direction


    def get_speed(self):
        return self._speed


    def is_moving(self):
        return self._moving


    def set_direction(self, direction):
        self._direction = direction


    def set_position(self, position):
        self._position = position


    def displace(self, displacement):
        self._position += displacement


    def enable_moving(self, value):
        self._moving = value

