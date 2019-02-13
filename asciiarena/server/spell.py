class Spell:
    def __init__(self, spell_spec, from_entity, position, direction):
        self._spec = spell_spec
        self._from_entity = from_entity
        self._position = position
        self._direction = direction


    def get_spec():
        return this._spec


    def get_origin_entity():
        return self._from_entity


    def get_position():
        return position


    def get_direction(self):
        return self._direction


    def set_position(self, position):
        self._position = position


    def move(self, displacement):
        self._position += displacement


    def set_direction(self, direction):
        self._direction = direction


    def clear_last_attemps(self):
        self._last_attempt_to_move = Vec2.zero()
