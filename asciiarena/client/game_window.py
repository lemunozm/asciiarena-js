from common.terrain import Terrain
from common.util.vec2 import Vec2

import time

class GameWindow:
    def __init__(self, screen, arena_size, ground, seed, character_list):
        self._screen = screen
        self._arena_size = arena_size
        self._ground = ground
        self._seed = seed
        self._character_list = character_list


    def update(self, entity_list, spell_list):

        self._screen.clear()

        self._draw_ground()
        self._draw_entities(entity_list)
        self._draw_debug_info()

        self._screen.render()


    def _draw_ground(self):
        pencil = self._screen.create_pencil(self._get_arena_origin())

        for i, terrain in enumerate(self._ground):
            position = Vec2(i % self._arena_size * 2, i / self._arena_size)
            if terrain == Terrain.EMPTY:
                pass
            elif terrain == Terrain.BORDER_WALL:
                pencil.draw(position, "X")
            elif terrain == Terrain.BLOCKED:
                pencil.draw(position, ".")
            else:
                pencil.draw(position, "?")


    def _draw_entities(self, entity_list):
        pencil = self._screen.create_pencil(self._get_arena_origin())

        for entity in entity_list:
            pencil.draw(Vec2(entity.position.x * 2, entity.position.y), entity.character)


    def _draw_debug_info(self):
        pencil = self._screen.create_pencil(self._get_debug_origin())
        pencil.draw(Vec2(0, 0), "FPS: {}".format(0))


    def _get_arena_origin(self):
        x = (self._screen.get_width() - self._arena_size * 2) / 2
        y = (self._screen.get_height() - self._arena_size) / 2

        return Vec2(x, y)


    def _get_debug_origin(self):
        return Vec2(0, 0)

