import pynput
import sys
import enum
import threading

class Key(enum.Enum):
    A = enum.auto()
    D = enum.auto()
    S = enum.auto()
    W = enum.auto()


class TypeEvent(enum.Enum):
    PRESSED = enum.auto()
    RELEASED = enum.auto()


class Keyboard:
    def __init__(self):
        self._listener = pynput.keyboard.Listener(on_press = self._on_press, on_release = self._on_release)
        self._listener.start()
        self._mutex = threading.Lock()
        self._global_key_pressed_list = []
        self._global_key_released_list = []
        self._global_key_set = set()
        self._local_key_set = set()


    def close(self):
        self._listener.stop()


    def is_key_down(self, key):
        return key in self._local_key_set


    def update_key_events(self, local_key_list):
        # Update local set
        for local_key in local_key_list:
            key = Keyboard._local_key_to_common_key(local_key)
            if key:
                self._local_key_set.add(key)

        with self._mutex:
            # Update global set with pressed events
            for key in self._global_key_pressed_list:
                self._global_key_set.add(key)

            # Update local with global information
            local_key_to_remove_list = []
            for key in self._local_key_set:
                if not key in self._global_key_set:
                    local_key_to_remove_list.append(key)

            for key in local_key_to_remove_list:
                self._local_key_set.remove(key)

            # Update global set with released events
            for key in self._global_key_released_list:
                self._global_key_set.remove(key)

            self._global_key_pressed_list = []
            self._global_key_released_list = []


    def _on_press(self, global_key):
        key = Keyboard._global_key_to_common_key(global_key)
        if key:
            with self._mutex:
                self._global_key_pressed_list.append(key)


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

