from common import version, message

import socket
import _pickle as pickle

class Client:
    def __init__(self, ip, port):
        self._ip = ip;
        self._port = port;

    def init(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self._ip, self._port))

        version_obj = message.Version(version.CURRENT)
        version_message = pickle.dumps(version_obj)
        sock.send(version_message)

        checked_version_message = sock.recv(message.MAX_BUFFER_SIZE)
        checked_version_obj = pickle.loads(checked_version_message)

