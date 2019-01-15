class GameManager:
    def __init__(self, player_registry, map_size, seed):
        self._player_registry = player_registry
        self._map_size = map_size
        self._seed = seed

    def get_map_size(self):
        return self._map_size

    def get_seed(self):
        return self._seed

    def init_game(self):
        print("init game")
