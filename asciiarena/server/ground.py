from common.util.vec2 import Vec2
from common.terrain import Terrain
from common.direction import Direction

import random

FREE_SPACE_PROPORTION = 0.1

class Ground:
    def __init__(self, size, seed):
        self._grid = [0 for i in range(size * size)]
        self._dimension = size
        self._seed = seed


    @staticmethod
    def fromSeed(size, seed):
        ground = Ground(size, seed)
        ground._generate()
        ground._create_border()
        return ground


    @staticmethod
    def fromFile(file):
        raise NotImplementedError()


    def set_at(self, position, terrain):
        self._grid[position.y * self._dimension + position.x] = terrain


    def get_at(self, position):
        return self._grid[position.y * self._dimension + position.x]


    def fill_at(self, position, dimension, terrain):
        for x in range(position.x, position.x + dimension.x):
            for y in range(position.y, position.y + dimension.y):
                self.set_at(Vec2(x, y), terrain)


    def get_grid_coordinates(self, index):
        return Vec2(index % self._dimension, int(index / self._dimension))


    def is_inside(self, position):
        return 0 <= position.x and position.x < self._dimension and 0 <= position.y and position.y < self._dimension


    def get_grid(self):
        return self._grid


    def get_dimension(self):
        return self._dimension


    def get_size(self):
        return self._dimension * self._dimension


    def get_seed(self):
        return self._seed


    def get_blocked_size(self):
        blocked_size = 0
        for terrain in self._grid:
            if Terrain.is_blocked(terrain):
                blocked_size += 1

        return blocked_size


    def get_empty_size(self):
        return self.get_size() - self.get_blocked_size()


    def is_blocked(self, position):
        return Terrain.is_blocked(self.get_at(position))


    def is_terrain(self, position, filter_terrain_list):
        return Terrain.is_any(self.get_at(position), filter_terrain_list)


    def is_empty_square(self, center, half_side, filter_terrain_list):
        for x in range(-half_side, half_side + 1):
            for y in range(-half_side, half_side + 1):
                position = center + Vec2(x, y)
                if self.is_inside(position) and self.is_terrain(position, filter_terrain_list):
                    return False

        return True


    def get_position_list(self, filter_terrain_list):
        empty_position_list = []
        for i, terrain in enumerate(self._grid):
            if Terrain.is_any(terrain, filter_terrain_list):
                position = self.get_grid_coordinates(i)
                empty_position_list.append(position)

        return empty_position_list


    def get_neighbour_list(self, position, filter_terrain_list, directions):
        neighbour_list = []

        for direction_vec in Direction.as_vector_list(directions):
            neighbour = position + direction_vec
            if self.is_inside(neighbour) and self.is_terrain(neighbour, filter_terrain_list):
                neighbour_list.append(neighbour)

        return neighbour_list


    def has_neighbours(self, position, filter_terrain_list, directions):
        for direction_vec in Direction.as_vector_list(directions):
            neighbour = position + direction_vec
            if self.is_inside(neighbour) and self.is_terrain(neighbour, filter_terrain_list):
                return True

        return False


    def find_separated_positions(self, amount, min_distance):
        random.seed(None)
        position_list = []
        free_terrain = []
        for i, terrain in enumerate(self._grid):
            if terrain == Terrain.EMPTY:
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
        self.fill_at(Vec2(0, 0), Vec2(self._dimension, 1), Terrain.BORDER_WALL)
        self.fill_at(Vec2(0, self._dimension - 1), Vec2(self._dimension, 1), Terrain.BORDER_WALL)
        self.fill_at(Vec2(0, 1), Vec2(1, self._dimension - 1), Terrain.BORDER_WALL)
        self.fill_at(Vec2(self._dimension - 1, 1), Vec2(1, self._dimension - 1), Terrain.BORDER_WALL)


    def _generate(self):
        random_engine = random.Random(self._seed)

        available_coordinates_list = self.get_position_list([Terrain.EMPTY])

        while 0.5 < len(available_coordinates_list) / self.get_size():
            wall_size = random_engine.randrange(0, 20)
            position = random_engine.choice(available_coordinates_list)
            self.set_at(position, Terrain.WALL_SEED)

            remaining_wall_size = len(available_coordinates_list) - int(self.get_size() * FREE_SPACE_PROPORTION)
            if remaining_wall_size < 0:
                break

            valid_wall_size = wall_size if wall_size < remaining_wall_size else remaining_wall_size

            for i in range(0, valid_wall_size):
                neighbour_list = self.get_neighbour_list(position, [Terrain.EMPTY], Direction.ANY)
                if neighbour_list:
                    position = random_engine.choice(neighbour_list)
                    self.set_at(position, Terrain.WALL_SEED)
                else:
                    break

            for i, terrain in enumerate(self._grid):
                if Terrain.is_any(terrain, [Terrain.EMPTY]):
                    position = self.get_grid_coordinates(i)
                    if self.has_neighbours(position, [Terrain.WALL_SEED], Direction.ANY):
                        self.set_at(position, Terrain.WALL)

            for i, terrain in enumerate(self._grid):
                if Terrain.is_any(terrain, [Terrain.WALL_SEED]):
                    self._grid[i] = Terrain.WALL

            available_coordinates_list = self.get_position_list([Terrain.EMPTY])

        print(self.get_empty_size())
        print(len(available_coordinates_list) / self.get_size())
