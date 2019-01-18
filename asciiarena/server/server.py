from .processor import Processor
from .game_manager import GameManager, Reply

import socket
import logging
import queue
from threading import Thread, Lock
import _pickle as pickle

logger = logging.getLogger("asciiarena")

class Server:
    def __init__(self, max_players, points, map_size, seed):
        self._game_manager = GameManager(max_players, points, map_size, seed)
        self._processor = GameProcessor(self._game_manager)
        self._processor.run()

    def get_processor():
        return self._processor

    def run(self, port):
        try:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind(("0.0.0.0", port))
            server_socket.listen()

            logger.info("Server listening on port: {}".format(port))

            while True:
                client_socket, (client_ip, client_port) = server_sock.accept()
                thread = Thread(target = self.handle_client_connections, args = (client_socket,))
                thread.start()
                logger.info("New connection from {}:{}".format(client_ip, client_socket))

        except OSError as error:
            logger.critical("Problem initializing the server, error: {}".format(error.errno))
            if(98 == error.errno):
                logger.critical("Port {} is already in use".format(port))

        finally:
            server_sock.close()

    def handle_client_connection(self, client_socket):
        try:
            (client_ip, client_port) = client_socket.getpeername()
            while True:
                client_request = Server._receive_message_from_client(client_socket)
                server_reply_list = self._processor.queue_request(client_request)

                for server_reply in server_reply_list:
                    Server._send_message_to_clients(server_reply)

        except OSError:
            logger.error("Connection lost with client {}:{}".format(client_ip, client_port))
            server_reply_list = self._processor.queue_request(message.Logout())

        finally:
            client_socket.close()

    def receive_message_from_client(client_socket):
        try:
            data = client_socket.recv(message.MAX_MESSAGE_SIZE)
            message = pickle.loads(data)
            print_message(message, "from", client_socket)
            return message
        except:
            raise OSError()

    def send_message_to_clients(message, client_socket_list):
        try:
            data = pickle.dumps(message)
            for client_socket in client_socket_list:
                client_socket.send(data)
                print_message(message, "to", client_socket)
        except:
            raise OSError()

    def print_message(message, direcction, sock):
        (client_ip, client_port) = client_socket.getpeername()
        logger.debug("{}: {} - {} {}:{}".format(obj.__class__.__name__, vars(obj), direcction, ip, port))

