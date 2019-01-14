from common import version, message

import socket
import _pickle as pickle

class Client:
    def __init__(self, ip, port, character):
        self._ip = ip;
        self._port = port;
        self._character = character

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self._ip, self._port))

        if not self._check_version(sock):
            return

        self._check_game_info(sock)
        self._login(sock)

    def _check_version(self, sock):
        version_obj = message.Version(version.CURRENT)
        version_message = pickle.dumps(version_obj)
        sock.send(version_message)

        checked_version_message = sock.recv(message.MAX_BUFFER_SIZE)
        checked_version_obj = pickle.loads(checked_version_message)

        compatibility = "COMPATIBLE" if checked_version_obj.validation else "INCOMPATIBLE"
        print("Connected to server {}:{}".format(self._ip, self._port))
        print("Client version: {} - server version: {} - {}".format(version.CURRENT, checked_version_obj.value, compatibility))

        return compatibility

    def _check_game_info(self, sock):
        pass

    def _login(self, sock):
        pass
