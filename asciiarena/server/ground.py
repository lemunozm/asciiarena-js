from common.util.vec2 import Vec2
from common.terrain import Terrain
from common.direction import Direction

import random

GEN_WALL_PROPORTION = 0.75
GEN_MIN_BLOCK_DISTANCE = 3
GEN_MIN_BLOCK_LEN = 1
GEN_MAX_BLOCK_LEN = 10
GEN_MIN_BLOCK_CHUNK = 1
GEN_MAX_BLOCK_CHUNK = 8

class Ground:
    def __init__(self, size, seed):
        self._grid = [0 for i in range(size * size)]
        self._dimension = size
        self._seed = seed


    @staticmethod
    def fromSeed(size, seed):
        ground = Ground(size, seed)
        ground._create_border()
        ground._generate_internal_walls()
        ground._wall_wrapping()
        return ground


    @staticmethod
    def fromFile(file):
        raise NotImplementedError()


    def set_at(self, position, terrain):
        self._grid[position.y * self._dimension + position.x] = terrain


    def get_at(self, position):
        if self.is_inside(position):
            return self._grid[position.y * self._dimension + position.x]
        else:
            return Terrain.OUTSIDE


    def fill_at(self, position, dimension, terrain):
        for x in range(position.x, position.x + dimension.x):
            for y in range(position.y, position.y + dimension.y):
                self.set_at(Vec2(x, y), terrain)


    def get_grid_coordinates_of(self, index):
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


    def get_neighbour_list(self, position, filter_terrain_list, direction_list):
        neighbour_list = []

        for direction_vec in Direction.as_vector_list(direction_list):
            neighbour = position + direction_vec
            if self.is_terrain(neighbour, filter_terrain_list):
                neighbour_list.append(neighbour)

        return neighbour_list


    def has_neighbours(self, position, filter_terrain_list, direction_list):
        check_list = [False] * len(filter_terrain_list)

        neighbour_list = self.get_neighbour_list(position, filter_terrain_list, direction_list)
        for neighbour in neighbour_list:
            terrain = self.get_at(neighbour)
            check_list[filter_terrain_list.index(terrain)] = True

        return check_list.count(False) == 0


    def has_any_neighbours(self, position, filter_terrain_list, direction_list):
        for direction_vec in Direction.as_vector_list(direction_list):
            neighbour = position + direction_vec
            if self.is_terrain(neighbour, filter_terrain_list):
                return True

        return False


    def has_all_neighbours(self, position, filter_terrain_list, direction_list):
        for direction_vec in Direction.as_vector_list(direction_list):
            neighbour = position + direction_vec
            if not self.is_terrain(neighbour, filter_terrain_list):
                return False

        return True


    def has_all_neighbours_distance(self, center, filter_terrain_list, distance, direction = None):
        left = -distance * int(direction != Direction.RIGHT)
        right = distance * int(direction != Direction.LEFT) + 1
        up = -distance * int(direction != Direction.DOWN)
        down = distance * int(direction != Direction.UP) + 1

        for x in range(left, right):
            for y in range(up, down):
                if x == 0 and y == 0:
                    continue

                position = center + Vec2(x, y)
                if not self.is_terrain(position, filter_terrain_list):
                    return False

        return True


    def get_position_list(self, filter_terrain_list):
        position_list = []
        for i, terrain in enumerate(self._grid):
            if Terrain.is_any(terrain, filter_terrain_list):
                position = self.get_grid_coordinates_of(i)
                position_list.append(position)

        return position_list


    def get_position_list_distance(self, filter_terrain_list, distance):
        position_list = []
        for i, terrain in enumerate(self._grid):
            position = self.get_grid_coordinates_of(i)
            if self.has_all_neighbours_distance(position, filter_terrain_list, distance):
                position_list.append(position)

        return position_list


    def find_separated_positions(self, amount, min_distance):
        random.seed(None)
        position_list = []
        free_terrain = []
        for i, terrain in enumerate(self._grid):
            if terrain == Terrain.EMPTY:
                free_terrain.append(self.get_grid_coordinates_of(i))

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


    def _generate_internal_walls(self):
        random_engine = random.Random(self._seed)

        available_coordinates_list = self.get_position_list_distance([Terrain.EMPTY], GEN_MIN_BLOCK_DISTANCE)

        while 1 - GEN_WALL_PROPORTION < len(available_coordinates_list) / self.get_size():
            block_len_list = range(GEN_MIN_BLOCK_LEN, GEN_MAX_BLOCK_LEN)
            wall_size_list = random_engine.sample(block_len_list, random_engine.randrange(GEN_MIN_BLOCK_CHUNK, GEN_MAX_BLOCK_CHUNK))
            wall_direction = random_engine.choice(Direction.ORTHOGONAL_LIST)
            direction = wall_direction
            position = random_engine.choice(available_coordinates_list)
            self.set_at(position, Terrain.WALL_SEED)

            for wall_size in wall_size_list:
                direction_vec = Direction.as_vector(direction)
                for i in range(0, wall_size):
                    new_position = position + direction_vec
                    if self.is_inside(new_position) and self.has_all_neighbours_distance(new_position, [Terrain.EMPTY], GEN_MIN_BLOCK_DISTANCE, direction):
                        position = new_position
                        self.set_at(position, Terrain.WALL_SEED)
                    else:
                        break

                direction = wall_direction if direction != wall_direction else random_engine.choice(Direction.get_orthogonal_list(direction))

            available_coordinates_list = self.get_position_list_distance([Terrain.EMPTY], GEN_MIN_BLOCK_DISTANCE)


    def _wall_wrapping(self):
        for i, terrain in enumerate(self._grid):
            if Terrain.is_any(terrain, [Terrain.EMPTY]):
                position = self.get_grid_coordinates_of(i)
                if self.has_any_neighbours(position, [Terrain.WALL_SEED, Terrain.BORDER_WALL], Direction.ALL_LIST):
                    self._grid[i] = Terrain.WALL

