from .mobile import Mobile
from .arena_element import ArenaElement

class Spell(ArenaElement):
    def __init__(self, spell_spec, from_entity, position, direction):
        super().__init__(position)
        self._spec = spell_spec
        self._from_entity = from_entity


    def get_spec():
        return self._spec


    def get_origin_entity():
        return self._from_entity


    def update(self, state):
        super().update_movement(state.get_ground(), state.get_entity_list())
        raise NotImplementedError()
