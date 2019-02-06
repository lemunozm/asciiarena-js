from common.terrain import Terrain
from common.util.vec2 import Vec2

import random

class Ground:
    def __init__(self, size, seed):
        self._grid = [0 for i in range(size * size)]
        self._size = size
        self._seed = seed


    @staticmethod
    def fromSeed(size, seed):
        ground = Ground(size, seed)
        ground._create_border()
        ground._generate()
        return ground


    @staticmethod
    def fromFile(file):
        raise NotImplementedError()


    def set_at(self, position, terrain):
        self._grid[position.y * self._size + position.x] = terrain


    def get_at(self, position):
        return self._grid[position.y * self._size + position.x]


    def is_blocked(self, position):
        terrain = self.get_at(position)
        return (terrain == Terrain.EMPTY_BLOCKED
            or terrain == Terrain.WALL
            or terrain == Terrain.BORDER_WALL)


    def fill_at(self, position, dimension, terrain):
        for x in range(position.x, position.x + dimension.x):
            for y in range(position.y, position.y + dimension.y):
                self.set_at(Vec2(x, y), terrain)


    def get_grid(self):
        return self._grid


    def get_size(self):
        return self._size


    def get_seed(self):
        return self._seed


    def get_grid_coordinates(self, index):
        return Vec2(index % self._size, int(index / self._size))


    def find_separated_positions(self, amount, min_distance):
        random.seed(None)
        position_list = []
        free_terrain = []
        for i, terrain in enumerate(self._grid):
            if Terrain.EMPTY == terrain:
                free_terrain.append(self.get_grid_coordinates(i))

        index = random.randrange(0, len(free_terrain))
        new_position = free_terrain[index]
        position_list.append(new_position)
        del free_terrain[index]

        while len(position_list) < amount:
            index = random.randrange(0, len(free_terrain))
            new_position = free_terrain[index]
            for position in position_list:
                if Vec2.distance(position, new_position) > min_distance:
                    position_list.append(new_position)
                    del free_terrain[index]
                    break

        return position_list


    def _create_border(self):
        self.fill_at(Vec2(0, 0), Vec2(self._size, 1), Terrain.BORDER_WALL)
        self.fill_at(Vec2(0, self._size - 1), Vec2(self._size, 1), Terrain.BORDER_WALL)
        self.fill_at(Vec2(0, 1), Vec2(1, self._size - 1), Terrain.BORDER_WALL)
        self.fill_at(Vec2(self._size - 1, 1), Vec2(1, self._size - 1), Terrain.BORDER_WALL)

    def _generate(self):
        self.set_at(Vec2(1, 1), Terrain.WALL)
        self.set_at(Vec2(2, 1), Terrain.WALL)
        self.set_at(Vec2(3, 1), Terrain.WALL)
        self.set_at(Vec2(1, 2), Terrain.WALL)
        self.set_at(Vec2(2, 2), Terrain.WALL)
        self.set_at(Vec2(3, 2), Terrain.WALL)

        self.set_at(Vec2(5, 5), Terrain.WALL)
        self.set_at(Vec2(6, 5), Terrain.WALL)
        self.set_at(Vec2(5, 6), Terrain.WALL)
        self.set_at(Vec2(6, 6), Terrain.WALL)

        self.set_at(Vec2(8, 5), Terrain.WALL)
        self.set_at(Vec2(9, 5), Terrain.WALL)
        self.set_at(Vec2(10, 5), Terrain.WALL)
        self.set_at(Vec2(8, 6), Terrain.WALL)
        self.set_at(Vec2(9, 6), Terrain.WALL)
        self.set_at(Vec2(10, 6), Terrain.WALL)
        self.set_at(Vec2(8, 7), Terrain.WALL)
        self.set_at(Vec2(9, 7), Terrain.WALL)
        self.set_at(Vec2(10, 7), Terrain.WALL)

        self.set_at(Vec2(5, 9), Terrain.WALL)
        self.set_at(Vec2(6, 9), Terrain.WALL)
        self.set_at(Vec2(7, 9), Terrain.WALL)
        self.set_at(Vec2(4, 10), Terrain.WALL)
        self.set_at(Vec2(5, 10), Terrain.WALL)
        self.set_at(Vec2(6, 10), Terrain.WALL)
        self.set_at(Vec2(7, 10), Terrain.WALL)
        self.set_at(Vec2(4, 11), Terrain.WALL)
        self.set_at(Vec2(5, 11), Terrain.WALL)
        self.set_at(Vec2(6, 11), Terrain.WALL)
        self.set_at(Vec2(7, 11), Terrain.WALL)
        self.set_at(Vec2(4, 12), Terrain.WALL)
        self.set_at(Vec2(5, 12), Terrain.WALL)
        self.set_at(Vec2(6, 12), Terrain.WALL)

