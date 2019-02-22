from .mobile import Mobile

class ArenaElement(Mobile):
    def __init__(self, position):
        Mobile.__init__(self, position)
        self._remove = False


    def remove(self):
        self._remove = True


    def must_be_removed(self):
        return self._remove


    def on_added_to_arena(self, arena_state):
        raise NotImplementedError()


    def update(self, arena_state):
        raise NotImplementedError()


