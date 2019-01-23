from common.logging import logger
from common.package_factory import PackageFactory
from common.package_queue import InputPack

from enum import Enum
import selectors
import socket
import threading

MAX_BUFFER_SIZE = 4096
BLOCKING_TIME = 0.05

class NetworkCommunication:
    class Operation(Enum):
        ACCEPT = 1
        READ = 2
        WRITE = 3

    def __init__(self, package_queue):
        self._selector = selectors.DefaultSelector()
        self._package_factory = PackageFactory()
        self._package_queue = package_queue
        self._disconnection_callback = None
        self._running = False

    def set_disconnection_callback(self, callback):
        self._disconnection_callback = callback

    def run(self):
        self._running = True

        self._input_thread = threading.Thread(target = self._input_process)
        self._input_thread.daemon = True
        self._input_thread.start()

        self._output_thread = threading.Thread(target = self._output_process)
        self._output_thread.daemon = True
        self._output_thread.start()

    def stop(self):
        self._running = False
        self._input_thread.join()
        self._output_thread.join()
        current_connection_list = []
        for key, value in self._selector.get_map().items():
            current_connection_list.append(value.fileobj)

        for connection in current_connection_list:
            self._close_connection(connection)

    def is_running(self):
        return self._running

    def listen(self, port):
        try:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.setblocking(False)
            server_socket.bind(("0.0.0.0", port))
            server_socket.listen()
            self._selector.register(server_socket, selectors.EVENT_READ, self.Operation.ACCEPT)

            logger.info("Listening on port: {}".format(port))
            return server_socket

        except OSError as error:
            logger.critical("Problem initializing the server on port {}, error: {}".format(port, error.errno))
            if(98 == error.errno):
                logger.critical("Port {} is already in use".format(port))
            return None

    def connect(self, ip, port):
        try:
            connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            connection.connect((ip, port))
            connection.setblocking(False)
            self._selector.register(connection, selectors.EVENT_READ, self.Operation.READ)

            logger.info("New connection to {}:{}".format(ip, port))
            return connection

        except OSError as error:
            logger.critical("Can not connect to {}:{}, error: {}".format(ip, port, error.errno))
            return None

    def _input_process(self):
        while self._running:
            for key, event in self._selector.select(timeout = BLOCKING_TIME):
                if self.Operation.ACCEPT == key.data:
                    connection, (ip, port) = key.fileobj.accept()
                    connection.setblocking(False)
                    logger.debug("New connection to {}:{}".format(ip, port))
                    self._selector.register(connection, selectors.EVENT_READ, self.Operation.READ)

                elif self.Operation.READ == key.data:
                    connection = key.fileobj
                    ip, port = connection.getpeername()
                    data = connection.recv(MAX_BUFFER_SIZE)
                    if data:
                        for input_pack in self._package_factory.create_input_packages(data, connection):
                            logger.debug("Message - {}: {} - from {}:{}".format(input_pack.message.__class__.__name__, vars(input_pack.message), ip, port))
                            self._package_queue.enqueue_input(input_pack)
                    else:
                        self._close_connection(connection)

    def _output_process(self):
        while self._running:
            output_pack = self._package_queue.dequeue_output(BLOCKING_TIME)
            if not output_pack:
                continue

            if output_pack.message:
                for data, connection in self._package_factory.process_output_package(output_pack):
                    try:
                        connection.sendall(data)
                        ip, port = connection.getpeername()
                        logger.debug("Message - {}: {} - to {}:{}".format(output_pack.message.__class__.__name__, vars(output_pack.message), ip, port))
                    except OSError:
                        pass
            else:
                for connection in output.endpoint_list:
                    self._close_connection(connection)

    def _close_connection(self, connection):
        ip, port = connection.getpeername()
        logger.debug("Connection closed with {}:{}".format(ip, port))
        if self._disconnection_callback:
            self._disconnection_callback(connection)

        self._package_queue.enqueue_input(InputPack("", connection))
        self._selector.unregister(connection)
        connection.close()

