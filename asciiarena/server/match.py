from .ground import Ground

class Match:
    def __init__(self, size, seed):
        self._ground = Ground.fromSeed(size, seed)

    def character_moves(self, character, direction):
        pass

    def character_shoots(self, character, skill_id):
        pass

    def get_ground(self):
        return self._ground

    def has_finished(self):
        return False
