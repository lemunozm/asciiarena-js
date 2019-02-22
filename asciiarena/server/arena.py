from .ground import Ground
from .entity import Entity
from .control import PlayerControl
from .arena_state import ArenaState
from .arena_grid import ArenaGrid

from common.direction import Direction
from common.util.vec2 import Vec2

class Arena:
    def __init__(self, dimension, seed):
        self._ground = Ground.fromSeed(dimension, seed)
        self._player_list = []
        self._entity_list = []
        self._spell_list = []
        self._grid = ArenaGrid(Vec2(dimension, dimension))
        self._step = 0


    def compute_player_origins(self, size):
        return self._ground.find_separated_positions(size, 5) # TODO: check the minimum distance


    def create_player(self, character, position):
        entity = Entity(character, position)
        entity.set_direction(Direction.DOWN)

        control = PlayerControl(entity)
        entity.set_control(control)

        self._player_list.append(entity)
        return control


    def get_ground(self):
        return self._ground


    def get_entity_list(self):
        return self._entity_list


    def get_spell_list(self):
        return self._spell_list


    def has_finished(self):
        return False #Check the _player_list


    def get_step(self):
        return self._step


    def update(self):
        state = ArenaState(self._step, self._ground, self._grid)

        if self._step == 0:
            for player in self._player_list:
                state.add_entity(player)

        for element in self._entity_list + self._spell_list:
            self._grid.remove(element)
            element.update(state)
            self._grid.add(element)

        self._entity_list = self._update_element_list(self._entity_list, state.get_new_entity_list())
        self._spell_list = self._update_element_list(self._spell_list, state.get_new_spell_list())

        self._step += 1


    def _update_element_list(self, old_element_list, new_element_list):
        next_element_list = []
        for element in old_element_list:
            if not element.must_be_removed():
                next_element_list.append(element);
            else:
                self._grid.remove(element)

        for element in new_element_list:
            if not element.must_be_removed():
                next_element_list.append(element)

        return next_element_list

