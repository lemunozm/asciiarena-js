from common.terrain import Terrain

import curses

class GameScreen:
    def __init__(self, arena_size):
        self._arena_size = arena_size
        self._stdscr = None


    def __enter__(self):
        self._stdscr = curses.initscr()
        self._stdscr.keypad(1)
        self._stdscr.nodelay(True)

        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        curses.start_color()

        for i in range(1, curses.COLORS):
            curses.init_pair(i, i, 0)

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


    def clear(self):
        self._stdscr.clear()


    def render(self):
        self._stdscr.refresh()


    def draw_ground(self, ground):
        x_origin = int((self.get_width() - self._arena_size * 2) / 2)
        y_origin = int((self.get_height() - self._arena_size) / 2)

        visual_ground = ""
        for i, terrain in enumerate(ground):
            if terrain == Terrain.EMPTY:
                pass
            elif terrain == Terrain.BORDER_WALL:
                self._stdscr.addstr(y_origin + int(i / self._arena_size), x_origin + i % self._arena_size * 2, "X")
            elif terrain == Terrain.BLOCKED:
                self._stdscr.addstr(y_origin + int(i / self._arena_size), x_origin + i % self._arena_size * 2, ".")
            else:
                self._stdscr.addstr(y_origin + int(i / self._arena_size), x_origin + i % self._arena_size * 2, "?")


    def draw_entities(self, entity_list):
        x_origin = int((self.get_width() - self._arena_size * 2) / 2)
        y_origin = int((self.get_height() - self._arena_size) / 2)

        for entity in entity_list:
            self._stdscr.addstr(y_origin + int(entity.position.y), x_origin + int(entity.position.x * 2), entity.character)


    def debug_draw_frame_stamp(self, stamp):
        x_origin = int((self.get_width() - self._arena_size * 2) / 2)
        y_origin = int((self.get_height() - self._arena_size) / 2) - 1

        self._stdscr.addstr(y_origin + self._arena_size + 2, x_origin, "Current frame stamp: {}".format(stamp))

