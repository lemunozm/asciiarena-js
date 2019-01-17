from .room import PlayerRoom
import threading

class GameManager:
    def __init__(self, max_players, points, map_size, seed):
        self._player_room = PlayerRoom(max_players, points);
        self._map_size = map_size
        self._seed = seed
        self._mutex = threading.Lock()

    def register_player(self, character, client):
        if self._player_room.add_player(character, client):
            logger.info("Player registered '{}' successfully".format(character))
            return message.PlayerLoginStatus.SUCCESFUL
        else:
            if self._player_room.is_open() or not self._player_room.is_complete():
                logger.info("Player registry try '{}': game closed".format(character))
                return message.PlayerLoginStatus.GAME_CLOSED
            else:
                logger.info("Player registry try '{}': already exists".format(character))
                return message.PlayerLoginStatus.ALREADY_EXISTS

    def unregister_player(self, character, client):
        # check that the client be the same
        pass



