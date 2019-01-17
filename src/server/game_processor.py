
class Processor:
    def __init__(self, game_manager):
        self._request_queue = []
        self._reply_queue = []

    def run(self):
        #Arrancar thread y leer de request_queue
            = dispatcher
        pass

    def dispatcher(self, request_data):
        if message.Version == request_message.__class__:
            return self._processor.version_request(sock, request_message)

        elif message.PlayerLogin == request_message.__class__:
            return self._processor.login_request(sock, request_message)

        elif message.PlayerAction == request_message.__class__:
            return self._processor.player_action_request(sock, request_message)

        else:
            raise ProcessingError("Unknown message received, rejecting connection...")

    def version_request(sender, version_message):
        validation = version.check(version_message.value)
        self._reply_queue.append(self._create_checked_version_reply())

        if validation:
            logger.info("Client request with version {}".format(version_message.value))
            self._reply_queue.append(self._create_game_info_reply())
        else:
            logger.warning("Client request with version {}: compatibility problems, rejected".format(version_message.value))

    def login_request(sender, login_message):
        status = self._game_manager.register_player(login_message.character, sender)
        self._reply_queue.append(self._create_login_status_reply())

        if message.PlayerLoginStatus.SUCCESFUL == status:
            self._reply_queue.append(self._create_game_info_reply())

        if self._game_manager.ready_to_start():
            self._request_queue.append(message.StartGame())

    def logout_request(sender, logout_message):
        if self._game_manager.unregister_player(login_message.character, sender):
            reply_list.append(self._create_game_info_reply())

    def start_game_request(sender, start_game_message):
        pass

    def player_action_request(sender, action_message):
        pass

    def _create_checked_version_reply(self, sender, validation):
        checked_version_message = message.CheckedVersion(version.CURRENT, validation)
        return Reply(checked_version_message, [sender])

    def _create_game_info_reply(self, sender):
        character_list = self._game_manager.get_room().get_character_list()
        max_players = self._game_manager.get_room().player_room.get_max_participants()
        points = self._game_manager.get_room().get_points_to_win()
        map_size = self._game_manager.get_map_size()
        seed = self._game_manager.get_seed()

        game_info_message = message.GameInfo(character_list, max_players, points, map_size, seed)
        return Reply(game_info_message, [sender])

    def _create_login_status_reply(self, sender):
        login_status_message = message.LoginStatus(status)
        return Reply(login_status_message, [sender])

    def _create_player_info_reply(self):
        players_info_message = message.PlayersInfo(self._game_manager.get_room().get_character_list())
        return Reply(players_info_message, self._game_manager.get_room().get_client_list())

