from common.terrain import Terrain
from common.util.vec2 import Vec2
from .screen import Style

import time

class GameScene:
    def __init__(self, screen, arena_size, ground, seed, character_list):
        self._screen = screen
        self._arena_size = arena_size
        self._ground = ground
        self._seed = seed
        self._character_list = character_list

        self._frame_counter = 0
        self._fps_time_stamp = 0
        self._fps = 0


    def update(self, entity_list, spell_list):
        self._screen.clear()
        self._draw_ground()
        self._draw_entities(entity_list)
        self._draw_debug_info()
        self._screen.render()


    def _draw_ground(self):
        pencil = self._screen.create_pencil(self._get_arena_origin())

        for i, terrain in enumerate(self._ground):
            position = Vec2((i % self._arena_size) * 2, i / self._arena_size)
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
            pencil.draw(Vec2(entity.position.x * 2, entity.position.y), entity.character, style = Style.BOLD)


    def _draw_debug_info(self):
        pencil = self._screen.create_pencil(self._get_debug_origin())

        current_time = time.time()
        self._frame_counter += 1
        if current_time - self._fps_time_stamp > 1.0:
            self._fps = self._frame_counter
            self._fps_time_stamp = current_time
            self._frame_counter = 0

        pencil.draw(Vec2(0, 0), "FPS: {:2d} - Seed: '{}'".format(self._fps, self._seed))


    def _get_arena_origin(self):
        x = (self._screen.get_width() - self._arena_size * 2) / 2
        y = (self._screen.get_height() - self._arena_size) / 2
        return Vec2(x, y)


    def _get_debug_origin(self):
        return Vec2(0, 0)

