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


    def update(self, state):
        super().update_movement(state.get_ground(), state.get_entity_list())


    def on_mobile_collision(self, entity):
        self.on_entity_collision(entity)
        return True


    def on_ground_collision(self, position, terrain):
        if terrain == Terrain.OUTSIDE or terrain == Terrain.BORDER_WALL or terrain == Terrain.WALL_SEED:
            self.enable_movement(False)
            return True
        else:
            return self.on_wall_collision(position, terrain)


    def on_entity_collision(self, entity):
        raise NotImplementedError()


    def on_wall_collision(self, wall_position, terrain):
        raise NotImplementedError()



