from common.util.vec2 import Vec2

import curses

class TermPencil:
    class Style:
        NORMAL = curses.A_NORMAL
        DIM = curses.A_DIM
        BOLD = curses.A_BOLD
        UNDERLINE = curses.A_UNDERLINE


    def __init__(self, stdscr, position):
        self._stdscr = stdscr
        self._origin = position
        self._color = 15
        self._style = TermPencil.Style.NORMAL


    def set_origin(self, origin):
        self._origin = origin


    def set_move(self, movement):
        self._origin += movement


    def set_color(self, color):
        self._color = color


    def set_style(self, style):
        self._style = style


    def draw(self, position, string, color = None, style = None):
        screen_pos = self._origin + position

        color = color if color != None else self._color
        style = style if style != None else self._style

        self._stdscr.addstr(int(screen_pos.y), int(screen_pos.x), string, curses.color_pair(color) | style)

