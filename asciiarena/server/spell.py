from .mobile import Mobile
from .arena_element import ArenaElement


class Spell(ArenaElement):
    def __init__(self, spell_spec, entity, position):
        ArenaElement.__init__(self, position)
        self._spec = spell_spec
        self._entity = entity


    def get_spec(self):
        return self._spec


    def get_origin_entity(self):
        return self._entity


    def on_added_to_arena(self, state):
        collide = state.get_ground().is_blocked(self._position)
        if not collide:
            initialized = self.on_init(state)
            if initialized:
                entity = state.get_grid().get_entity(self._position)
                if entity:
                    self.on_entity_collision(state, entity)

            return  initialized

        return False


    def update(self, state):
        previous_position = self._position.copy()

        super().compute_movement()
        if self._position != previous_position:
            if state.get_ground().is_blocked(self._position):
                self._position = previous_position
                self.on_wall_collision(state, self._position)

            else:
                entity = state.get_grid().get_entity(self._position)
                if entity:
                    self.on_entity_collision(state, entity)

        self.on_update(state)


    def on_init(self, state):
        raise NotImplementedError()


    def on_update(self, state):
        raise NotImplementedError()


    def on_wall_collision(self, state, position):
        raise NotImplementedError()


    def on_entity_collision(self, state, entity):
        raise NotImplementedError()

