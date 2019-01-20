import selectors
import socket
import _pickle as pickle
import threading

class NetworkCommunication:
    def __init__(self, package_queue):
        self._selector = selectors.DefaultSelector()
        self._package_queue = package_queue

    def add_server_socket(server_socket):
        self._selector.register(server_socket, selectors.EVENT_READ, _accept)

    def add_connection(connection):
        self._selector.register(connection, selectors.EVENT_READ, _read)

    def remove_connection(connection):
        self._selector.unregister(connection)

    def run(self):
        input_thread = Thread(target = self._input_process)
        input_thread.start()

        output_thread = Thread(target = self._output_process)
        output_thread.start()

    def _input_process(self):
        for key, mask in mysel.select(timeout=1):
            callback = key.data
            callback(key.fileobj, mask)

    def _output_process(self):
        message, connection = self._package_queue.dequeue_output()
        data = pickle.dumps(mesage)
        rv = connection.sendall()
        print("Send - {}".format(rv))

    def _accept(self, server_socket, mask):
        connection, address = server_socket.accept()
        connection.setblocking(False)
        self.add_connection(connection)

    def _read(self, connection, mask):
        client_address = connection.getpeername()
        print('read({})'.format(client_address))
        data = connection.recv(1024)
        if data:
            print('  received {!r}'.format(data))
            message = pickle.loads(data)
            self._package_queue.enqueue_input((message, connection))
        else:
            print('  closing')
        pass

