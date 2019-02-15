from .mobile import Mobile

class Spell(Mobile):
    def __init__(self, spell_spec, from_entity, position, direction):
        Mobile.__init__(self, position)
        self._control = spell_spec.create_control()
        self._spec = spell_spec
        self._from_entity = from_entity


    def get_spec():
        return self._spec


    def get_control(self):
        return self._control


    def get_origin_entity():
        return self._from_entity

