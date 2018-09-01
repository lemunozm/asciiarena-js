package com.asciiarena.lib.server;

import com.asciiarena.lib.common.logging.Log;

public class Server
{
    private ServerConfig config;

    public Server(final ServerConfig config)
    {
        this.config = config;
        Log.init();
    }

    public void run()
    {
        GameServer gameServer = new GameServer(config.game);

        Runnable gameServerRun = new Runnable() 
        {
            @Override
            public void run() {
                gameServer.listen();
            }
        };  

        new Thread(gameServerRun).start();

        InfoServer infoServer = new InfoServer(config.info, gameServer);
        infoServer.listen();
    }
}
