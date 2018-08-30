package com.asciiarena.server;

import com.asciiarena.common.logging.Log;

public class Server
{
    private ServerConfig config;

    public Server(ServerConfig config)
    {
        this.config = config;
        Log.init();
    }

    public void run()
    {
        GameServer gameServer = new GameServer(config.game);

        Runnable gameServerRun = new Runnable() 
        {
            public void run() {
                gameServer.run();
            }
        };  

        Thread gameServerThread = new Thread(gameServerRun);
        gameServerThread.start();

        InfoServer infoServer = new InfoServer(config.info, gameServer);
        infoServer.run();
    }
}
