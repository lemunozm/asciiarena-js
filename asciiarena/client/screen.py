from .pencil import TermPencil
from common.util.vec2 import Vec2

import curses
import enum
import time

class TermScreen:
    def __init__(self):
        self._stdscr = curses.initscr()
        self._stdscr.keypad(1)
        self._stdscr.nodelay(True)

        self._fps_position = None
        self._frame_counter = 0
        self._fps_time_stamp = 0
        self._fps = 0

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


    def enable_fps_counter(self, position):
        self._fps_position = position


    def create_pencil(self, position):
        return TermPencil(self._stdscr, position)


    def clear(self):
        self._stdscr.erase()


    def draw(self):
        self._draw_fps()
        self._stdscr.refresh()
        self._stdscr.move(self.get_height() - 2, 0) #Allow using print function after drawing


    def _draw_fps(self):
        if not self._fps_position:
            return

        pencil = self.create_pencil(self._fps_position)

        current_time = time.time()
        self._frame_counter += 1
        if current_time - self._fps_time_stamp > 1.0:
            self._fps = self._frame_counter
            self._fps_time_stamp = current_time
            self._frame_counter = 0

        pencil.draw(Vec2(0, 0), "FPS: {:2d}".format(self._fps))

