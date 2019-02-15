from .mobile import Mobile

class Entity(Mobile):
    def __init__(self, character, position):
        Mobile.__init__(self, position)
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


    def cast(self, skill):
        self._last_skill = skill


    def add_buff(self, buff):
        pass


    def remove_buff(self, buff):
        pass

