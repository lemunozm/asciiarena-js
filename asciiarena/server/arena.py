from .ground import Ground
from .entity import Entity
from .control import PlayerControl
from .arena_element import ArenaState

from common.direction import Direction

class Arena:
    def __init__(self, dimension, seed):
        self._ground = Ground.fromSeed(dimension, seed)
        self._player_list = []
        self._entity_list = []
        self._spell_list = []
        self._step = 0


    def compute_player_origins(self, size):
        return self._ground.find_separated_positions(size, 5) # TODO: check the minimum distance


    def create_player(self, character, position):
        entity = Entity(character, position)
        entity.set_direction(Direction.DOWN)

        control = PlayerControl(entity)
        entity.set_control(control)

        self._entity_list.append(entity)
        self._player_list.append(entity)
        return control


    def get_ground(self):
        return self._ground


    def get_entity_list(self):
        return self._entity_list


    def has_finished(self):
        return False #Check the player_list


    def get_step_number():
        return self._step


    def update(self):
        state = ArenaState(self._step, self._ground, self._entity_list.copy(), self._spell_list.copy())

        for arena_element in self._entity_list + self._spell_list:
            arena_element.update(state)

        self._entity_list = [entity for entity in state.get_entity_list() if not entity.must_be_removed()]
        self._spell_list = [spell for spell in state.get_spell_list() if not spell.must_be_removed()]

        self._step += 1

