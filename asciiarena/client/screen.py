from .pencil import TermPencil

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
        return TermPencil(self._stdscr, position)


    def clear(self):
        self._stdscr.erase()


    def render(self):
        self._stdscr.refresh()
        self._stdscr.move(self.get_height() - 2, 0) #Allow using print function afther the render

