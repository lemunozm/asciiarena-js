import socket
from . import message
import _pickle as pickle

def send(sock, object):
    data = pickle.dumps(object)
    sock.send(data)

def recv(sock):
    data = sock.recv(message.MAX_BUFFER_SIZE)
    return pickle.loads(data)

def sendAll(sock_list, object):
    data = pickle.dumps(object)
    for sock in sock_list:
        sock.send(data)

def recvAll(sock_list):
    object_list = []
    for sock in sock_list:
        data = sock.recv(message.MAX_BUFFER_SIZE)
        object_list.append(pickle.loads(data))
    return object_list
