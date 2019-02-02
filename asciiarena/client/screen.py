from common.terrain import Terrain
from common.util.vec2 import Vec2

import curses
import enum

class TermScreen:
    def __init__(self):
        self._stdscr = curses.initscr()
        self._stdscr.keypad(1)
        self._stdscr.nodelay(True)

        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        curses.start_color()

        for i in range(1, curses.COLORS):
            curses.init_pair(i, i, 0)


    def __enter__(self):
        return self


    def __exit__(self ,type, value, traceback):
        self._stdscr.keypad(0)
        curses.echo()
        curses.nocbreak()
        curses.endwin()
        curses.flushinp()


    def get_width(self):
        return curses.COLS


    def get_height(self):
        return curses.LINES


    def get_size(self):
        return Vec2(self.get_width(), self.get_height())


    def get_event_list(self):
        key_event_list = []
        while True:
            key_event = self._stdscr.getch()
            if key_event == curses.ERR:
                break
            key_event_list.append(key_event)
        return key_event_list


    def create_pencil(self, position):
        return Pencil(self._stdscr, position)


    def clear(self):
        self._stdscr.clear()


    def render(self):
        self._stdscr.refresh()


class Style:
    NORMAL = curses.A_NORMAL
    DIM = curses.A_DIM
    BOLD = curses.A_BOLD
    UNDERLINE = curses.A_UNDERLINE


class Pencil:
    def __init__(self, stdscr, position):
        self._stdscr = stdscr
        self._origin = position
        self._color = 15
        self._style = Style.NORMAL


    def set_origin(self, origin):
        self._origin = origin


    def set_color(self, color):
        self._color = color


    def set_style(self, style):
        self._style = style


    def draw(self, position, string, color = None, style = None):
        x_pos = int(self._origin.x + position.x)
        y_pos = int(self._origin.y + position.y)

        color = color if color != None else self._color
        style = style if style != None else self._style

        self._stdscr.addstr(y_pos, x_pos, string, curses.color_pair(color) | style)

