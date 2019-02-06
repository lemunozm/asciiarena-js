from common.terrain import Terrain
from common.util.vec2 import Vec2
from .screen import Style
from . import gui_utils
from .gui_utils import PathFragment

import time

class GameScene:
    def __init__(self, screen, character, arena_size, ground, seed, character_list):
        self._screen = screen
        self._player_character = character
        self._last_player_direction = Vec2.zero()
        self._arena_size = arena_size
        self._ground = ground
        self._seed = seed
        self._character_list = character_list

        self._frame_counter = 0
        self._fps_time_stamp = 0
        self._fps = 0


    def update(self, entity_list, spell_list, player_direction):
        self._screen.clear()
        self._draw_player_direction(entity_list, player_direction)
        self._draw_ground_border()
        self._draw_ground_walls()
        self._draw_entities(entity_list)
        self._draw_debug_info()
        self._screen.render()


    def _draw_ground_border(self):
        pencil = self._screen.create_pencil(self._get_arena_origin())
        pencil.set_color(33)
        pencil.set_style(Style.DIM)

        border_image = gui_utils.create_path_image([Terrain.BORDER_WALL], self._ground, Vec2(self._arena_size, self._arena_size))

        for i, border in enumerate(border_image):
            position = Vec2((i % self._arena_size) * 2, int(i / self._arena_size))
            if PathFragment.includes(border, PathFragment.VERTICAL):
                pencil.draw(position, "│")
            elif PathFragment.includes(border, PathFragment.HORIZONTAL):
                pencil.draw(position, "──")
            elif border == PathFragment.CORNER_LEFT_UP:
                pencil.draw(position, "╭─")
            elif border == PathFragment.CORNER_LEFT_DOWN:
                pencil.draw(position, "╰─")
            elif border == PathFragment.CORNER_RIGHT_UP:
                pencil.draw(position, "╮")
            elif border == PathFragment.CORNER_RIGHT_DOWN:
                pencil.draw(position, "╯")


    def _draw_ground_walls(self):
        pencil = self._screen.create_pencil(self._get_arena_origin())
        pencil.set_color(139)
        pencil.set_style(Style.DIM)

        wall_image = gui_utils.create_path_image([Terrain.WALL], self._ground, Vec2(self._arena_size, self._arena_size))

        for i, wall in enumerate(wall_image):
            position = Vec2((i % self._arena_size) * 2, int(i / self._arena_size))
            if wall == PathFragment.ALL:
                continue
            elif wall == PathFragment.CORNER_LEFT_UP_EXTEND:
                pencil.draw(position, "╭─")
            elif wall == PathFragment.CORNER_LEFT_DOWN_EXTEND:
                pencil.draw(position, "╰─")
            elif wall == PathFragment.CORNER_RIGHT_UP_EXTEND:
                pencil.draw(position, "╮")
            elif wall == PathFragment.CORNER_RIGHT_DOWN_EXTEND:
                pencil.draw(position, "╯")
            elif PathFragment.includes(wall, PathFragment.VERTICAL):
                pencil.draw(position, "│")
            elif PathFragment.includes(wall, PathFragment.HORIZONTAL):
                pencil.draw(position, "──")
            elif PathFragment.includes(wall, PathFragment.CORNER_LEFT_UP):
                pencil.draw(position, "╭─")
            elif PathFragment.includes(wall, PathFragment.CORNER_LEFT_DOWN):
                pencil.draw(position, "╰─")
            elif PathFragment.includes(wall, PathFragment.CORNER_RIGHT_UP):
                pencil.draw(position, "╮")
            elif PathFragment.includes(wall, PathFragment.CORNER_RIGHT_DOWN):
                pencil.draw(position, "╯")


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
                pencil.draw(Vec2(point.x * 2, point.y), "·", 240, Style.BOLD)
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

