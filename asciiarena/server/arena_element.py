from .mobile import Mobile

class ArenaState:
    def __init__(self, step, ground, entity_list, spell_list):
        self._step = step
        self._ground = ground
        self._entity_list = entity_list
        self._spell_list = spell_list

    def get_step(self):
        return self._step


    def get_ground(self):
        return self._ground


    def get_entity_list(self):
        return self._entity_list


    def get_spell_list(self):
        return self._spell_list


    def add_entity(self, entity):
        self._entity_list.append(entity)


    def add_spell(self, spell):
        self._spell_list.append(spell)


    def get_entity_at(self, position):
        for entity in self._entity_list:
            if entity.get_position() == position:
                return entity

        return None


class ArenaElement(Mobile):
    def __init__(self, position):
        super().__init__(position)
        self._remove = False


    def remove(self):
        self._remove = True


    def must_be_removed(self):
        return self._remove


    def update(self, arena_state):
        raise NotImplementedError()


