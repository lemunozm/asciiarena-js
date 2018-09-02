package com.asciiarena.lib.server;

import java.io.IOException;
import java.net.ServerSocket;
import java.net.Socket;

import com.asciiarena.lib.common.communication.Connection;
import com.asciiarena.lib.common.communication.Message;
import com.asciiarena.lib.common.logging.Log;
import com.asciiarena.lib.common.version.Version;

public class Server
{
    private final int port;
    private GameManager gameManager;
    private boolean gameStarted;

    public Server(ServerConfig config)
    {
        Log.init(null);
        this.port = config.port;
        this.gameManager = new GameManager(config.game);
        this.gameStarted = false;
    }

    public void listen()
    {
        try(ServerSocket serverSocket = new ServerSocket(port))
        {
            while (true) 
            {
                Socket socket = serverSocket.accept();
                Runnable clientConnectionRun = new Runnable() 
                {
                    @Override
                    public void run() 
                    {
                        clientConnection(socket);
                    }
                };  

                new Thread(clientConnectionRun).start();
            } 
        } 
        catch (IOException e)
        {
            e.printStackTrace();
        }
    }

    private void clientConnection(Socket socket)
    {
        Connection connection = new Connection(socket);

        if(!checkClientConnection(connection))
        {
            connection.close();
            return;
        }

        Message.NewPlayer newPlayerMessage = (Message.NewPlayer) connection.receive();
        synchronized(this)
        {
            if(!gameManager.login(newPlayerMessage.character, connection))
            {
                connection.close();
                return;
            }

            if(gameManager.getPlayerRegistry().isComplete())
            {
                initGame();
            }
        }
    }

    private boolean checkClientConnection(Connection connection)
    {
        if(checkVersion(connection))
        {
            sendServerInfo(connection);
            if(!gameManager.getPlayerRegistry().isComplete())
            {
                return true;
            }
        }

        return false;
    }

    private boolean checkVersion(Connection connection)
    {
        Message.Version versionMessage = (Message.Version) connection.receive();

        Message.CheckedVersion checkedVersionMessage = new Message.CheckedVersion();
        checkedVersionMessage.version = Version.CURRENT;
        checkedVersionMessage.validation = validateVersion(versionMessage.version);
        connection.send(checkedVersionMessage);

        return checkedVersionMessage.validation;
    }

    private boolean validateVersion(String version)
    {
        switch(Version.check(version))
        {
            case OK:
                return true;
            case WARNING:
                Log.warning("Version request: compatible, but are not the same: client is %s and server is %s", version, Version.CURRENT);
                return true;
            case ERROR:
                Log.error("Version request: incompatible: client is %s and server is %s", version, Version.CURRENT);
            default:
                return false;
        }
    }

    private void sendServerInfo(Connection connection)
    {
        Message.ServerInfo serverInfoMessage = new Message.ServerInfo();
        serverInfoMessage.players = gameManager.getPlayerRegistry().getCharacters();
        serverInfoMessage.maxPlayers = gameManager.getPlayerRegistry().getMaxPlayers();
        connection.send(serverInfoMessage);
    }

    private void initGame()
    {
        Runnable gameRun = new Runnable() 
        {
            @Override
            public void run() 
            {
                gameStarted = true;
                gameManager.startGame();
                gameStarted = false;
            }
        };  

        new Thread(gameRun).start();
    }

    public int getPort()
    {
        return port;
    }

    public GameManager getGameManager()
    {
        return gameManager;
    }

    public boolean isGameStarted()
    {
        return gameStarted;
    }
}
