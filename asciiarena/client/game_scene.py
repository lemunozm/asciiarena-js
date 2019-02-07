from .pencil import TermPencil
from .box_drawing import BoxLine, BoxLineDrawing

from common.util.vec2 import Vec2
from common.terrain import Terrain

import time

class GameScene:
    def __init__(self, screen, character, arena_size, ground, seed, character_list):
        self._screen = screen
        self._player_character = character
        self._last_player_direction = Vec2.zero()
        self._arena_size = arena_size
        self._arena_dimension = Vec2(arena_size, arena_size)
        self._ground = ground
        self._seed = seed
        self._character_list = character_list

        self._frame_counter = 0
        self._fps_time_stamp = 0
        self._fps = 0


    def update(self, entity_list, spell_list, player_direction):
        self._screen.clear()
        self._draw_player_direction(entity_list, player_direction)
        self._draw_ground_walls()
        self._draw_entities(entity_list)
        self._draw_debug_info()
        self._screen.render()


    def _draw_ground_walls(self):
        pencil = self._screen.create_pencil(self._get_arena_origin())
        pencil.set_color(33)
        pencil.set_style(TermPencil.Style.DIM)

        box_drawing = BoxLineDrawing(pencil, BoxLineDrawing.Style.SINGLE_ROUND)

        line_table = BoxLine.parse([Terrain.BORDER_WALL, Terrain.WALL], self._ground, self._arena_dimension)
        box_drawing.draw(line_table, self._arena_dimension, Vec2(2, 1))


    def _draw_entities(self, entity_list):
        pencil = self._screen.create_pencil(self._get_arena_origin())

        for entity in entity_list:
            pencil.draw(Vec2(entity.position.x * 2, entity.position.y), entity.character)


    def _draw_player_direction(self, entity_list, direction):
        pencil = self._screen.create_pencil(self._get_arena_origin())

        if Vec2.zero() == direction:
            return

        for entity in entity_list:
            if entity.character == self._player_character:
                point = entity.position + direction
                pencil.draw(Vec2(point.x * 2, point.y), "·", 240, TermPencil.Style.BOLD)
                return


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

