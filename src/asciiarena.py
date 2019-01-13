import client
import server

import sys

def init_client(argv):
    game_client = client.Client("127.0.0.1", 2009)
    game_client.init()

def init_server(argv):
    game_server = server.Server(2009)
    game_server.run()

if __name__ == '__main__':
    if sys.argv[1] == "client":
        init_client(sys.argv)
    elif sys.argv[1] == "server":
        init_server(sys.argv)

