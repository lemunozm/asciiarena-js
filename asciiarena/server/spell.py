from .mobile import Mobile
from .arena_element import ArenaElement

from common.terrain import Terrain

class Spell(ArenaElement):
    def __init__(self, spell_spec, from_entity, position):
        super().__init__(position)
        self._spec = spell_spec
        self._from_entity = from_entity


    def get_spec(self):
        return self._spec


    def get_origin_entity(self):
        return self._from_entity


    def on_mobile_collision(self, mobile):
        self.on_entity_collision(mobile)


    def update(self, state):
        super().update_movement(state.get_ground(), state.get_entity_list())


    def on_added_to_arena(self, state):
        return not super().check_collision(state.get_ground(), state.get_entity_list())


    def on_entity_collision(self, entity):
        pass


    def on_wall_collision(self, wall_position, terrain):
        pass

