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
        self._global_key_dict = {}
        self._local_key_dict = {}


    def close(self):
        self._listener.stop()


    def is_key_down(self, key):
        return self._local_key_dict.get(key, False)


    def update_key_events(self, local_key_list):
        # Update local dict
        for local_key in local_key_list:
            key = Keyboard._local_key_to_common_key(local_key)
            if key:
                self._local_key_dict[key] = True

        with self._mutex:
            # Update global dict with pressed events
            for key in self._global_key_pressed_list:
                self._global_key_dict[key] = True

            # Update local with global information
            local_key_to_remove_list = []
            for key in self._local_key_dict.keys():
                if not self._global_key_dict.get(key, False):
                    local_key_to_remove_list.append(key)

            for key in local_key_to_remove_list:
                self._local_key_dict.pop(key)

            # Update global dict with released events
            for key in self._global_key_released_list:
                self._global_key_dict[key] = False

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
        switcher = {
            97:  Key.A,
            100: Key.D,
            115: Key.S,
            119: Key.W,
        }
        return switcher.get(local_key, None)


    @staticmethod
    def _global_key_to_common_key(global_key):
        try:
            switcher_chars = {
                'a': Key.A,
                'd': Key.D,
                's': Key.S,
                'w': Key.W,
            }
            return switcher_chars.get(global_key.char, None)

        except AttributeError:
            return None

