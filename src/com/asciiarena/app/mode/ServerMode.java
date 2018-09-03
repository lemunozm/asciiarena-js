package com.asciiarena.app.mode;

import com.asciiarena.lib.common.logging.Log;
import com.asciiarena.lib.server.Server;
import com.asciiarena.lib.server.ServerConfig;

public class ServerMode
{
    public static void start(String[] args)
    {
        ServerConfig config = new ServerConfig();
        config.port = 3000;
        config.game.players = 4;
        config.game.pointsToWin = 1;
        config.game.map.width = 30;
        config.game.map.height = 30;
        config.game.map.seed = "";

        Log.init(null);

        Server server = new Server(config);
        server.listen();
    }
}
