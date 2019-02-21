from .pencil import TermPencil
from .keyboard import Keyboard, Key
from .box_drawing import BoxLine, BoxLineDrawing

from common.util.vec2 import Vec2
from common.direction import Direction
from common.terrain import Terrain

import time
import enum


class GameSceneEvent(enum.Enum):
    PLAYER_MOVEMENT = enum.auto()
    PLAYER_CAST = enum.auto()


class GameScene:
    def __init__(self, screen, character, character_list, arena_size, ground_grid, seed):
        self._screen = screen
        self._screen.enable_fps_counter(Vec2(0, 0))
        self._keyboard = Keyboard(screen)

        self._player_character = character
        self._character_list = character_list
        self._arena_dimension = Vec2(arena_size, arena_size)
        self._ground_grid = ground_grid
        self._seed = seed

        self._last_time_stamp_skill_key = 0
        self._skill_cast_try = False

        self._skill_cast_failure_cursor_counter = 0


    def compute_events(self):
        self._keyboard.update_key_events()

        player_event_list = []

        direction = self._check_player_movement_direction()
        if direction != Direction.NONE:
            player_event_list.append((GameSceneEvent.PLAYER_MOVEMENT, direction))

        self._skill_cast_try = False
        skill_id = self._check_player_cast_skill()
        if skill_id != 0:
            player_event_list.append((GameSceneEvent.PLAYER_CAST, skill_id))
            self._skill_cast_try = True

        return player_event_list


    def _check_player_movement_direction(self):
        movement_keys = {
            Key.W: Direction.UP,
            Key.A: Direction.LEFT,
            Key.S: Direction.DOWN,
            Key.D: Direction.RIGHT,
        }

        key, time_stamp = self._keyboard.get_last_key_down(list(movement_keys))
        return movement_keys.get(key, Direction.NONE)


    def _check_player_cast_skill(self):
        skill_keys = {
            Key.J: 1,
            Key.K: 2,
        }

        key, time_stamp = self._keyboard.get_last_key_down(list(skill_keys))
        if key != Key.NONE and time_stamp > self._last_time_stamp_skill_key:
            self._last_time_stamp_skill_key = time_stamp
            return skill_keys.get(key, 0)

        return 0


    def render(self, entity_list, spell_list):
        self.draw_ground_walls()
        self.draw_entities(entity_list)
        self.draw_spells(spell_list)
        self.draw_info()


    def draw_ground_walls(self):
        pencil = self._screen.create_pencil(self.get_arena_origin())
        pencil.set_color(33)
        pencil.set_style(TermPencil.Style.DIM)

        wall_list = [Terrain.BORDER_WALL, Terrain.WALL, Terrain.INTERNAL_WALL]
        line_table = BoxLine.parse(wall_list, self._ground_grid, self._arena_dimension)

        box_drawing = BoxLineDrawing(pencil, BoxLineDrawing.Style.SINGLE_ROUND)
        box_drawing.draw(line_table, self._arena_dimension, Vec2(2, 1))


    def draw_entities(self, entity_list):
        pencil = self._screen.create_pencil(self.get_arena_origin())

        for entity in entity_list:
            if Direction.NONE != entity.direction:
                point = entity.position + Direction.as_vector(entity.direction)
                cursor, color = ("·", 240)

                if entity.character == self._player_character:
                    if self._skill_cast_try:
                        if self.is_terrain_blocked(point):
                            self._skill_cast_failure_cursor_counter = 5
                    if self._skill_cast_failure_cursor_counter > 0:
                        cursor, color = ("×", 124)
                        self._skill_cast_failure_cursor_counter -= 1

                pencil.draw(Vec2(point.x * 2, point.y), cursor, color, TermPencil.Style.BOLD)

        for entity in entity_list:
            pencil.draw(Vec2(entity.position.x * 2, entity.position.y), entity.character)


    def draw_spells(self, spell_list):
        pencil = self._screen.create_pencil(self.get_arena_origin())

        for spell in spell_list:
            pencil.draw(Vec2(spell.position.x * 2, spell.position.y), "o", 208)


    def draw_info(self):
        pencil = self._screen.create_pencil(self.get_info_origin())
        pencil.draw(Vec2(0, 0), "Seed: '{}'".format(self._seed))


    def get_arena_origin(self):
        x = (self._screen.get_width() - self._arena_dimension.x * 2) // 2
        y = (self._screen.get_height() - self._arena_dimension.y) // 2
        return Vec2(int(x), int(y))


    def get_info_origin(self):
        return Vec2(0, 1)


    def is_terrain_blocked(self, position):
        return Terrain.is_blocked(self._ground_grid[position.y * self._arena_dimension.x + position.x])

