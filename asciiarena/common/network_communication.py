import selectors
import socket
import _pickle as pickle
import threading
import time

ACCEPT = 1
READ = 2

class NetworkCommunication:
    def __init__(self, package_queue):
        self._selector = selectors.DefaultSelector()
        self._package_queue = package_queue

    def listen(self, port):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.setblocking(False)
        server_socket.bind(('localhost', port))
        server_socket.listen()
        self._selector.register(server_socket, selectors.EVENT_READ, ACCEPT)
        return server_socket

    def connect(self, ip, port):
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection.connect((ip, port))
        connection.setblocking(False)
        self._selector.register(connection, selectors.EVENT_READ, READ)
        return connection

    def run(self):
        input_thread = threading.Thread(target = self._input_process)
        input_thread.start()

        output_thread = threading.Thread(target = self._output_process)
        output_thread.start()

    def _input_process(self):
        while True:
            for key, mask in self._selector.select():
                if ACCEPT == key.data:
                    print("New connection")
                    connection, address = key.fileobj.accept()
                    connection.setblocking(False)
                    self._selector.register(connection, selectors.EVENT_READ, READ)

                elif READ == key.data:
                    connection = key.fileobj
                    client_address = connection.getpeername()
                    print('read({})'.format(client_address))
                    time.sleep(5)
                    data = connection.recv(1024)
                    if data:
                        message = pickle.loads(data)
                        print('  received {}'.format(message))
                        self._package_queue.enqueue_input((message, connection))
                    else:
                        print('  closing')
                        self._selector.unregister(connection)
                        connection.close()

    def _output_process(self):
        while True:
            message, connection = self._package_queue.dequeue_output()
            if message:
                data = pickle.dumps(message)
                connection.sendall(data)
                print("Send returns {}".format(rv))
            else:
                print('  closing')
                self._selector.unregister(connection)
                connection.close()
