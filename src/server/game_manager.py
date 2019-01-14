class GameManager:
    def __init__(self, map_size, seed):
        self._map_size = map_size
        self._seed = seed

    def get_map_size(self):
        return self._map_size

    def get_seed(self):
        return self._seed
