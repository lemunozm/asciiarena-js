from .arena_element import ArenaElement

from .spells.fire_ball import FireBall # remove when skill works properly

class Entity(ArenaElement):
    def __init__(self, character, position):
        ArenaElement.__init__(self, position)
        self._control = None
        self._character = character
        self._buff_list = []


    def get_control(self):
        return self._control


    def set_control(self, control):
        self._control = control


    def get_character(self):
        return self._character


    def get_buff_list(self):
        return self._buff_list


    def get_cast_position(self):
        return self.get_position() + self.get_direction_vec()


    def cast(self, skill):
        return FireBall(int, self, self.get_cast_position())


    def add_buff(self, buff):
        pass


    def remove_buff(self, buff):
        pass


    def on_added_to_arena(self, state):
        collide = state.get_ground().is_blocked(self._position) or state.get_grid().get_entity(self._position)
        if not collide:
            if self._control:
                return self._control.on_init(state)

            return True

        return False


    def update(self, state):
        previous_position = self._position.copy()

        super().compute_movement()
        if self._position != previous_position:
            if state.get_ground().is_blocked(self._position):
                self._position = previous_position
                if self._control:
                    self._control.on_collision(state, self._position)

            else:
                entity = state.get_grid().get_entity(self._position)
                if entity:
                    self._position = previous_position
                    if self._control:
                        self._control.on_collision(state, self._position)

        if self._control:
            self._control.on_update(state)

