import client
import server
from common import version

import argparse
import sys
import string
import math

def command_line_interface():
    default_port = "3500"

    parser = argparse.ArgumentParser(prog = "asciiarena")
    parser.add_argument("--version", action = "version", version = "%(prog)s " + version.CURRENT)

    subparsers = parser.add_subparsers(title = "subcomands", help="select the application mode")

    client_parser = subparsers.add_parser("client")
    client_parser.add_argument("--ip", required = True, help = "Server ip")
    client_parser.add_argument("--port", default = default_port, type = int, help = "Server port (" + default_port + " by default)")
    client_parser.add_argument("--character", help = "Player character", choices = list(string.ascii_uppercase))
    client_parser.set_defaults(func = init_client)

    server_parser = subparsers.add_parser("server")
    server_parser.add_argument("--players", required = True, type = int, help = "required players to init a game")
    server_parser.add_argument("--port", default = default_port, type = int, help = "open the server in the specified port (" + default_port + " by default)")
    server_parser.add_argument("--points", default = 0, type = int, help = "necessary points for a player to win the game")
    server_parser.add_argument("--log", default = "none", choices=["info", "warning", "error", "none"], help = "Set the log level (none by default)")
    server_parser.add_argument("--map-size", default = 0, type = int, help = "size of the map")
    server_parser.add_argument("--seed", default = "", help = "map generator seed (random by default)")
    server_parser.set_defaults(func = init_server)

    args = parser.parse_args()
    args.func(args)

def init_client(args):
    print("Running asciiarena client...")

    game_client = client.Client(args.ip, args.port, args.character)
    game_client.run()

def init_server(args):
    print("Running asciiarena server...")

    points = args.points if 0 != args.points else args.players * 5
    map_size = args.map_size if 0 != args.map_size else int(math.sqrt(args.players * 255))

    game_server = server.Server(args.port, args.players, points, map_size, args.seed, args.log)
    game_server.run()

if __name__ == "__main__":
    command_line_interface()

