from common import version, message

import socket
import _pickle as pickle

class Server:
    def __init__(self, port):
        self._port = port

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('0.0.0.0', self._port))
        sock.listen()

        while True:
            connection, address = sock.accept()

            version_message = connection.recv(message.MAX_BUFFER_SIZE)
            version_obj = pickle.loads(version_message)

            validation = version.check(version_obj.value)

            checked_version_obj = message.CheckedVersion(version.CURRENT, validation)
            checked_version_message = pickle.dumps(checked_version_obj)
            connection.send(checked_version_message)

