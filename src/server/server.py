from common import version, message, communication
from .processor import Processor
from .game_manager import GameManager, Reply

import socket
import logging
from threading import Thread, Lock
import _pickle as pickle

logger = logging.getLogger("asciiarena")

class Server:
    def __init__(self, max_players, points, map_size, seed):
        self._game_manager = GameManager(max_players, points, map_size, seed)
        self._processor = Processor(self._game_manager)

    def get_game_manager():
        return self._game_manager

    def get_processor():
        return self._processor

    def run(self, port):
        try:
            server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_sock.bind(("0.0.0.0", port))
            server_sock.listen()

            logger.info("Server listening on port: {}".format(port))

            while True:
                sock, (client_ip, client_port) = server_sock.accept()
                logger.info("New connection from {}:{}".format(client_ip, client_port))
                thread = Thread(target = self.handle_client_connection, args = (sock,))
                thread.start()

        except OSError as error:
            logger.critical("Problem initializing the server, error: {}".format(error.errno))
            if(98 == error.errno):
                logger.critical("Port {} is already in use".format(port))

        finally:
            server_sock.close()

    def handle_client_connection(self, sock):
        try:
            (client_ip, client_port) = sock.getpeername()
            while True:
                client_request = self._receive_message_from_client(sock)
                server_reply_list = self._processor.queue_request(client_request)

                for server_reply in server_reply_list:
                    self._send_message_to_clients(server_reply)

        except communication.ConnectionLost:
            logger.error("Connection lost with client {}:{}".format(client_ip, client_port))

        finally:
            sock.close()

    def process_client_message(seld, sock, client_message):
        if message.Version == client_message.__class__:
            return self._processor.version_request(sock, client_message)

        elif message.PlayerLogin == client_message.__class__:
            return self._processor.login_request(sock, client_message)

        elif message.PlayerAction == client_message.__class__:
            return self._processor.player_action_request(sock, client_message)

        else:
            logger.warning("Unknown message received, rejecting connection...")
            raise communication.ConnectionLost()

    def receive_message_from_client(self, sock):
        request_message = pickle.loads(request_data)
        pass

    def send_message_to_clients(self, message, sock_list):
        pass
