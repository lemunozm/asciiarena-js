import client
import server
from common import version

import argparse
import sys
import string
import math
import logging

logger = logging.getLogger("asciiarena")

DEFAULT_PORT = "2500"

def command_line_interface():

    parser = argparse.ArgumentParser(prog = "asciiarena")
    parser.add_argument("--version", action = "version", version = "%(prog)s " + version.CURRENT)

    subparsers = parser.add_subparsers(title = "subcomands", help="select the application mode")

    client_parser = subparsers.add_parser("client")
    client_parser.add_argument("--ip", required = True, help = "Server ip")
    client_parser.add_argument("--port", default = DEFAULT_PORT, type = int, help = "Server port (" + DEFAULT_PORT + " by default)")
    client_parser.add_argument("--character", default = "", help = "Player character", choices = list(string.ascii_uppercase))
    client_parser.set_defaults(func = init_client)

    server_parser = subparsers.add_parser("server")
    server_parser.add_argument("--players", required = True, type = int, help = "required players to init a game")
    server_parser.add_argument("--port", default = DEFAULT_PORT, type = int, help = "open the server in the specified tcp port (" + DEFAULT_PORT + " by default)")
    server_parser.add_argument("--points", default = 0, type = int, help = "necessary points for a player to win the game")
    server_parser.add_argument("--log-level", default = "critical", choices=["none", "debug", "info", "warning", "error", "critical"], help = "Set the log level (critical by default)")
    server_parser.add_argument("--map-size", default = 0, type = int, help = "size of the map")
    server_parser.add_argument("--seed", default = "", help = "map generator seed (random by default)")
    server_parser.set_defaults(func = init_server)

    args = parser.parse_args()
    args.func(args)

def init_client(args):
    print("Running asciiarena client...")

    logger.disabled = True

    game_client = client.Client(args.ip, args.port, args.character)
    game_client.run()

def init_server(args):
    print("Running asciiarena server...")

    points = args.points if 0 != args.points else args.players * 5
    map_size = args.map_size if 0 != args.map_size else int(math.sqrt(args.players * 255))

    init_logger(args.log_level)

    game_server = server.Server(args.players, points, map_size, args.seed)
    game_server.run(args.port)

def init_logger(log_level):
    level = {
        "none": logging.NOTSET,
        "debug": logging.DEBUG,
        "info": logging.INFO,
        "warning": logging.WARNING,
        "error": logging.ERROR,
        "critical": logging.CRITICAL,
    }[log_level]

    logger.setLevel(level)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", "%Y-%m-%d %H:%M:%S")
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)

if __name__ == "__main__":
    command_line_interface()

