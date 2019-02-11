import pynput
import sys
import enum
import threading
import time

class Key(enum.Enum):
    A = enum.auto()
    D = enum.auto()
    S = enum.auto()
    W = enum.auto()


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


    def is_key_down(self, key):
        return self._key_dict.get(key, None)


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
    97:  Key.A,
    100: Key.D,
    115: Key.S,
    119: Key.W,
}

# From keylogger lib
_GLOBAL_KEY_DICT = {
    'a': Key.A,
    'd': Key.D,
    's': Key.S,
    'w': Key.W,
}

