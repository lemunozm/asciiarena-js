from .ground import Ground
from common.util.vec2 import Vec2

import time

class Entity:
    def __init__(self, ground, entity_list, character, position):
        self._const_ground = ground
        self._const_entity_list = entity_list

        self._character = character
        self._position = position
        self._direction = Vec2(0, 0)
        self._speed = 8

        self._last_move_timestamp = 0


    def get_character(self):
        return self._character


    def get_position(self):
        return self._position


    def set_position(self, position):
        self._position = position


    def displace(self, displacement):
        self._position += displacement


    def move(self, direction):
        current = time.time()
        if self._direction != direction:
            self._direction = direction
            new_position = self._position + self._direction
            #check collisions
            self._position = new_position
            self._last_move_timestamp = current

        elif current - self._last_move_timestamp > 1 / self._speed:
            new_position = self._position + self._direction
            #check collisions
            self._position = new_position
            self._last_move_timestamp = current

        return current == self._last_move_timestamp


class Arena:
    def __init__(self, size, seed, character_list):
        self._ground = Ground.fromSeed(size, seed)
        self._entity_list = []

        position_list = self._ground.find_separated_positions(len(character_list), 5) #check the minimum distance
        for i, character in enumerate(character_list):
            entity = Entity(self._ground, self._entity_list, character, position_list[i])
            self._entity_list.append(entity)


    def get_ground(self):
        return self._ground


    def get_entity_list(self):
        return self._entity_list


    def has_finished(self):
        return False


    def update(self):
        pass
