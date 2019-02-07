import enum
import math

class Vec2:
    def __init__(self, x, y):
        self.x = x
        self.y = y


    def __str__(self):
        return "Vec2({}, {})".format(self.x, self.y)


    def __eq__(self, v):
        if isinstance(v, Vec2):
            return self.x == v.x and self.y == v.y
        return False


    def __ne__(self, v):
        return not self.__eq__(v)


    def __add__(self, v):
        return Vec2(self.x + v.x, self.y + v.y)


    def __sub__(self, v):
        return Vec2(self.x - v.x, self.y - v.y)


    def __iadd__(self, v):
        self.x = self.x + v.x
        self.y = self.y + v.y
        return self


    def __isub__(self, v):
        self.x = self.x - v.x
        self.y = self.y - v.y
        return self


    def get_length(self):
        return math.sqrt(self.x**2 + self.y**2)


    @staticmethod
    def distance(v1, v2):
        return (v1 - v2).get_length()

    @staticmethod
    def zero():
        return Vec2(0, 0)
