import socket
import logging
from . import message
import _pickle as pickle
from pprint import pprint

logger = logging.getLogger("asciiarena")

class ConnectionLost(Exception):
    pass

TO = 1
FROM = 2
def print_message(direcction, ip, port, obj):
    direcction = "to" if TO else "from"
    logger.debug("{}: {} - {} {}:{}".format(obj.__class__.__name__, vars(obj), direcction, ip, port))

def print_connection_lost(direcction, ip, port):
    direcction = "sending to" if TO else "receiving from"
    logger.error("Connection lost {} {}:{}".format(direcction, ip, port))

def send(sock, obj):
    (ip, port) = sock.getpeername()
    try:
        data = pickle.dumps(obj)
        sock.send(data)
        print_message(TO, ip, port, obj)

    except (OSError, EOFError):
        print_connection_lost(TO, ip, port)
        raise ConnectionLost("Connection lost")

def recv(sock):
    (ip, port) = sock.getpeername()
    try:
        data = sock.recv(message.MAX_BUFFER_SIZE)
        obj = pickle.loads(data)
        print_message(FROM, ip, port, obj)
        return obj

    except (OSError, EOFError):
        print_connection_lost(FROM, ip, port)
        raise ConnectionLost("Connection lost")

def sendAll(sock_list, obj):
    data = pickle.dumps(obj)
    for sock in sock_list:
        (ip, port) = sock.getpeername()
        try:
            sock.send(data)
            print_message(TO, ip, port, obj)

        except (OSError, EOFError):
            print_connection_lost(TO, ip, port)
            raise ConnectionLost("Connection lost")

def recvAll(sock_list):
    obj_list = []
    for sock in sock_list:
        (ip, port) = sock.getpeername()
        try:
            data = sock.recv(message.MAX_BUFFER_SIZE)
            obj = pickle.loads(data)
            obj_list.append(obj)
            print_message(FROM, ip, port, obj)

        except (OSError, EOFError):
            print_connection_lost(FROM, ip, port)
            raise ConnectionLost("Connection lost")

    return obj_list

