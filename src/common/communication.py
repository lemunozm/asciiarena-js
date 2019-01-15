import socket
import _pickle as pickle

def send(sock, object):
    message = pickle.dumps(object)
    sock.send(message)

def recv(sock):
    message = sock.recv(message.MAX_BUFFER_SIZE)
    return pickle.loads(version_message)

def sendAll(sock, object):
    message = pickle.dumps(object)
    sock.send(message)

def recvAll(sock_list):
    object_list = []
    for sock in sock_list:
        message = sock.recv(message.MAX_BUFFER_SIZE)
        object_list.append(pickle.loads(version_message))
    return object_list
