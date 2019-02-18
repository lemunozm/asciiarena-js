from ..spell import Spell

from common.terrain import Terrain

class FireBall(Spell):
    def __init__(self, spell_spec, from_entity, position):
        super().__init__(spell_spec, from_entity, position)
        super().set_direction(from_entity.get_direction())
        super().enable_movement(True)

        super().set_speed(20)

    def update(self, state):
        super().update(state)


    def on_entity_collision(self, entity):
        # Damage to the entity
        super().remove()


    def on_wall_collision(self, wall_position, terrain):
        super().enable_movement(False)
        #super().remove()
        return False
