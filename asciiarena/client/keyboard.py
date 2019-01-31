import pynput
import sys
import enum
import threading

class Key(enum.Enum):
    A = enum.auto()
    UNKNOWN = enum.auto()


class Keyboard:
    def __init__(self):
        self._key_map = {}
        self._listener = pynput.keyboard.Listener(on_release = self._on_release)
        self._listener.start()
        self._mutex = threading.Lock()


    def close(self):
        self._listener.stop()


    def is_key_down(self, key):
        return self._key_map.get(key, False)


    def add_key_events(self, key_event_list):
        with self._mutex:
            for key_event in key_event_list:
                key = Keyboard._key_event_to_key(key_event)
                self._key_map[key] = True


    def _on_release(self, key_code):
        key = Keyboard._key_code_to_key(key_code)
        with self._mutex:
            self._key_map.pop(key, None)


    @staticmethod
    def _key_event_to_key(key_event):
        switcher = {
            97: Key.A,
        }
        return switcher.get(key_event, Key.UNKNOWN)


    @staticmethod
    def _key_code_to_key(key_code):
        switcher_chars = {
            'a': Key.A,
        }
        if key_code.char:
            return switcher_chars.get(key_code.char, Key.UNKNOWN)

        return Key.UNKNOWN

