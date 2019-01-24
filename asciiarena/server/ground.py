from common.terrain import Terrain

class Ground:
    def __init__(self, size, seed):
        self._grid = [0 for i in range(size * size)]
        self._size = size
        self._seed = seed

    @staticmethod
    def fromSeed(size, seed):
        ground = Ground(size, seed)
        ground._create_border()
        return ground

    @staticmethod
    def fromFile(file):
        raise NotImplementedError()

    def set_at(self, x, y, terrain):
        self._grid[y * self._size + x] = terrain

    def get_at(self, x, y):
        return self._grid[y * self._size + x]

    def fill_at(self, left, top, width, height, terrain):
        for x in range(left, left + width):
            for y in range(top, top + height):
                self.set_at(x, y, terrain)

    def get_grid(self):
        return self._grid

    def get_size(self):
        return self._size

    def get_seed(self):
        return self._seed

    def _create_border(self):
        self.fill_at(0, 0, self._size, 1, Terrain.BORDER_WALL)
        self.fill_at(0, self._size - 1, self._size, 1, Terrain.BORDER_WALL)
        self.fill_at(0, 1, 1, self._size - 1, Terrain.BORDER_WALL)
        self.fill_at(self._size - 1, 1, 1, self._size - 1, Terrain.BORDER_WALL)

