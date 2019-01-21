from common.logging import logger
from common.package_queue import InputPack, OutputPack

from enum import Enum
import selectors
import socket
import _pickle as pickle
import threading

MAX_BUFFER_SIZE = 4096

class NetworkCommunication:
    class Operation(Enum):
        ACCEPT = 1
        READ = 2
        WRITE = 3

    def __init__(self, package_queue):
        self._selector = selectors.DefaultSelector()
        self._package_queue = package_queue
        self._disconnection_callback = None
        self._running = False

    def listen(self, port):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.setblocking(False)
        server_socket.bind(('localhost', port))
        server_socket.listen()

        self._selector.register(server_socket, selectors.EVENT_READ, self.Operation.ACCEPT)
        return None

    def connect(self, ip, port):
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection.connect((ip, port))
        connection.setblocking(False)

        self._selector.register(connection, selectors.EVENT_READ, self.Operation.READ)
        return connection

    def set_disconnection_callback(self, callback):
        self._disconnection_callback = callback

    def run(self):
        self._running = True

        input_thread = threading.Thread(target = self._input_process)
        input_thread.daemon = True
        input_thread.start()

        output_thread = threading.Thread(target = self._output_process)
        output_thread.daemon = True
        output_thread.start()

    def close(self):
        self._running = False

    def is_running(self):
        return self._running

    def _input_process(self):
        while self._running:
            for key, event in self._selector.select(timeout = 1):
                if self.Operation.ACCEPT == key.data:
                    connection, (ip, port) = key.fileobj.accept()
                    connection.setblocking(False)
                    logger.debug("New connection with {}:{}".format(ip, port))
                    self._selector.register(connection, selectors.EVENT_READ, self.Operation.READ)

                elif self.Operation.READ == key.data:
                    connection = key.fileobj
                    ip, port = connection.getpeername()
                    data = connection.recv(MAX_BUFFER_SIZE)
                    if data:
                        message = pickle.loads(data)
                        logger.debug("Message {}: {} - from {}:{}".format(obj.__class__.__name__, vars(obj), ip, port))
                        self._package_queue.enqueue_input((message, connection))
                    else:
                        self._close_connection(connection)

    def _output_process(self):
        while self._running:
            output = self._package_queue.dequeue_output(1)
            if output:
                message, connection_list = output
                if message:
                    data = pickle.dumps(message)
                    for connection in connection_list:
                        ip, port = connection.getpeername()
                        if connection.send(data):
                            logger.debug("Message {}: {} - to {}:{}".format(obj.__class__.__name__, vars(obj), ip, port))
                        else:
                            self._close_connection(connection)
                else:
                    for connection in connection_list:
                        self._close_connection(connection)

    def _close_connection(self, connection):
        ip, port = connection.getpeername()
        logger.debug("Connection closed with {}:{}".format(ip, port))
        self._disconnection_callback(connection)
        self._selector.unregister(connection)
        connection.close()

