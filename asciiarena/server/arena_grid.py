from .entity import Entity
from .spell import Spell

from common.util.vec2 import Vec2

class ArenaGrid:
    class GridElement:
        def __init__(self):
            self.entity = None
            self.spell_list = []


    def __init__(self, dimension):
        self._dimension = dimension
        self._grid = {}

        for y in range(0, dimension.y):
            for x in range(0, dimension.x):
                self._grid[Vec2(x, y)] = ArenaGrid.GridElement()


    def get(self, position):
        return self._grid[position]


    def get_entity(self, position):
        return self._grid[position].entity


    def get_spell_list(self, position):
        return self._grid[position].spell_list


    def add(self, element):
        if element.__class__ == Entity:
            self._grid[element.get_position()].entity = element

        elif element.__class__ == Spell:
            self._grid[element.get_position()].spell_list.append(element)


    def remove(self, element):
        if element.__class__ == Entity:
            self._grid[element.get_position()].entity = None

        elif element.__class__ == Spell:
            self._grid[element.get_position()].spell_list.remove(element)


