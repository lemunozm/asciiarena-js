import pynput
import sys
import enum
import threading
import time
import math

class Key(enum.Enum):
    NONE = enum.auto()
    A = enum.auto()
    B = enum.auto()
    C = enum.auto()
    D = enum.auto()
    E = enum.auto()
    F = enum.auto()
    G = enum.auto()
    H = enum.auto()
    I = enum.auto()
    J = enum.auto()
    K = enum.auto()
    L = enum.auto()
    M = enum.auto()
    N = enum.auto()
    O = enum.auto()
    P = enum.auto()
    Q = enum.auto()
    R = enum.auto()
    S = enum.auto()
    T = enum.auto()
    U = enum.auto()
    V = enum.auto()
    W = enum.auto()
    X = enum.auto()
    Y = enum.auto()
    Z = enum.auto()


class TypeEvent(enum.Enum):
    PRESSED = enum.auto()
    RELEASED = enum.auto()


class Keyboard():
    def __init__(self, screen):
        self._screen = screen
        self._mutex = threading.Lock()
        self._global_key_released_list = []
        self._key_dict = {}
        self._persistant_key_dict = {}

        self._listener = pynput.keyboard.Listener(on_release = self._on_release)
        self._listener.start()


    def close(self):
        self._listener.stop()


    def is_key_down(self, key, default = 0):
        return self._key_dict.get(key, default)


    def is_key_list_down(self, key_list, default = 0):
        time_stamp_list = []
        for key in key_list:
            time_stamp_list.append(self._key_dict.get(key, default))

        return time_stamp_list


    def get_first_key_down(self, key_list):
        time_stamp_list = self.is_key_list_down(key_list, math.inf)
        min_time = min(time_stamp_list)
        if min_time < math.inf:
            return key_list[time_stamp_list.index(min_time)]

        return Key.NONE


    def get_last_key_down(self, key_list):
        time_stamp_list = self.is_key_list_down(key_list)
        max_time = max(time_stamp_list)
        if max_time > 0:
            return key_list[time_stamp_list.index(max_time)]

        return Key.NONE


    def update_key_events(self):
        with self._mutex:
            local_key_pressed_list = []
            for local_key in self._screen.get_event_list():
                pressed_key = Keyboard._local_key_to_common_key(local_key)
                if pressed_key:
                    local_key_pressed_list.append(pressed_key)

            for pressed_key in local_key_pressed_list:
                if pressed_key not in self._persistant_key_dict:
                    self._persistant_key_dict[pressed_key] = time.time()

            for released_key in self._global_key_released_list:
                self._persistant_key_dict.pop(released_key, None)

            self._global_key_released_list.clear()

        # Compute the keys that were pressed and released
        # into the interval between two updates
        self._key_dict = self._persistant_key_dict.copy()
        for pressed_key in local_key_pressed_list:
            if pressed_key not in self._key_dict:
                self._key_dict[pressed_key] = time.time()


    def _on_release(self, global_key):
        key = Keyboard._global_key_to_common_key(global_key)
        if key:
            with self._mutex:
                self._global_key_released_list.append(key)


    @staticmethod
    def _local_key_to_common_key(local_key):
        return _LOCAL_KEY_DICT.get(local_key, None)


    @staticmethod
    def _global_key_to_common_key(global_key):
        try:
            return _GLOBAL_KEY_DICT.get(global_key.char, None)

        except AttributeError:
            return None


# From curses lib
_LOCAL_KEY_DICT = {
    ord('a'): Key.A,
    ord('b'): Key.B,
    ord('c'): Key.C,
    ord('d'): Key.D,
    ord('e'): Key.E,
    ord('f'): Key.F,
    ord('g'): Key.G,
    ord('h'): Key.H,
    ord('i'): Key.I,
    ord('j'): Key.J,
    ord('k'): Key.K,
    ord('l'): Key.L,
    ord('m'): Key.M,
    ord('n'): Key.N,
    ord('o'): Key.O,
    ord('p'): Key.P,
    ord('q'): Key.Q,
    ord('r'): Key.R,
    ord('s'): Key.S,
    ord('t'): Key.T,
    ord('u'): Key.U,
    ord('v'): Key.V,
    ord('w'): Key.W,
    ord('x'): Key.X,
    ord('y'): Key.Y,
    ord('z'): Key.Z,
}

# From keylogger lib
_GLOBAL_KEY_DICT = {
    'a': Key.A,
    'b': Key.B,
    'c': Key.C,
    'd': Key.D,
    'e': Key.E,
    'f': Key.F,
    'g': Key.G,
    'h': Key.H,
    'i': Key.I,
    'j': Key.J,
    'k': Key.K,
    'l': Key.L,
    'm': Key.M,
    'n': Key.N,
    'o': Key.O,
    'p': Key.P,
    'q': Key.Q,
    'r': Key.R,
    's': Key.S,
    't': Key.T,
    'u': Key.U,
    'v': Key.V,
    'w': Key.W,
    'x': Key.X,
    'y': Key.Y,
    'z': Key.Z,
}

