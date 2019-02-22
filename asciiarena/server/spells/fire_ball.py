from ..spell import Spell

from common.terrain import Terrain

class FireBall(Spell):
    def __init__(self, spell_spec, entity, position):
        super().__init__(spell_spec, entity, position)
        super().set_direction(entity.get_direction())
        super().enable_movement(True)
        super().set_speed(20)


    def on_init(self, state):
        return True


    def on_update(self, state):
        pass


    def on_wall_collision(self, state, position):
        super().enable_movement(False)
        super().remove()


    def on_entity_collision(self, state, entity):
        super().remove()

