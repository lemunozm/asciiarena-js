from .pencil import TermPencil
from .box_drawing import BoxLine, BoxLineDrawing

from common.util.vec2 import Vec2
from common.terrain import Terrain

import time

FILL_BORDER = True
FILL_WALLS = True

class GameScene:
    def __init__(self, screen, character, arena_size, ground, seed, character_list):
        self._screen = screen
        self._player_character = character
        self._last_player_direction = Vec2.zero()
        self._arena_size = arena_size
        self._ground, self._ground_dimension = GameScene._init_ground(ground, arena_size)
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
        pencil = self._screen.create_pencil(self._get_ground_origin())
        pencil.set_color(33)
        pencil.set_style(TermPencil.Style.DIM)

        wall_list = [Terrain.BORDER_WALL, Terrain.WALL]
        if FILL_WALLS:
            wall_list.append(Terrain.WALL_SEED)

        line_table = BoxLine.parse(wall_list, self._ground, self._ground_dimension)

        box_drawing = BoxLineDrawing(pencil, BoxLineDrawing.Style.SINGLE_ROUND)
        box_drawing.draw(line_table, self._ground_dimension, Vec2(2, 1))


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


    def _get_ground_origin(self):
        x = (self._screen.get_width() - self._ground_dimension.x * 2) / 2
        y = (self._screen.get_height() - self._ground_dimension.y) / 2
        return Vec2(int(x), int(y))


    def _get_arena_origin(self):
        x = (self._screen.get_width() - self._arena_size * 2) / 2
        y = (self._screen.get_height() - self._arena_size) / 2
        return Vec2(int(x), int(y))


    def _get_debug_origin(self):
        return Vec2(0, 0)


    @staticmethod
    def _init_ground(ground, ground_size):
        terrain_base = Terrain.BORDER_WALL if FILL_BORDER else [Terrain.EMPTY]
        extended_ground_size = ground_size + 2
        extended_ground = [terrain_base] * (extended_ground_size * extended_ground_size)

        for y in range(0, ground_size):
            for x in range(0, ground_size):
                extended_ground[(y + 1) * extended_ground_size + (x + 1)] = ground[y * ground_size + x]

        return extended_ground, Vec2(extended_ground_size, extended_ground_size)
