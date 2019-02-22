class ArenaState:
    def __init__(self, step, ground, grid):
        self._step = step
        self._ground = ground
        self._grid = grid
        self._new_entity_list = []
        self._new_spell_list = []


    def get_step(self):
        return self._step


    def get_ground(self):
        return self._ground


    def get_grid(self):
        return self._grid


    def get_new_entity_list(self):
        return self._new_entity_list


    def get_new_spell_list(self):
        return self._new_spell_list


    def add_entity(self, entity):
        if entity.on_added_to_arena(self):
            self._new_entity_list.append(entity)
            self._grid.add(entity)


    def add_spell(self, spell):
        if spell.on_added_to_arena(self):
            self._new_spell_list.append(spell)
            self._grid.add(spell)


