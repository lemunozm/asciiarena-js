package com.asciiarena.lib.server;

import java.io.IOException;
import java.net.ServerSocket;

import com.asciiarena.lib.common.communication.Connection;

public class GameServer
{
    int port;
    GameManager gameManager;

    public GameServer(ServerConfig.GameConfig config)
    {
        this.port = config.port;
        this.gameManager = new GameManager(config);
    }

    public void listen()
    {
        try(ServerSocket serverSocket = new ServerSocket(port))
        {
            while (true) 
            {
                Connection connection = new Connection(serverSocket.accept());
                playerConnection(connection);
            } 
        }
        catch (IOException e)
        {
            e.printStackTrace();
        }
    }

    private void playerConnection(Connection connection)
    {
        if(gameManager.registerPlayer(connection))
        {
            if(gameManager.isReadyToStartGame())
            {
                Runnable gameRun = new Runnable() 
                {
                    @Override
                    public void run() {
                        gameManager.startGame();
                    }
                };  

                new Thread(gameRun).start();
            }
        }
    }

    public int getPort()
    {
        return port;
    }

    public GameManager getGameManager()
    {
        return gameManager;
    }
}
