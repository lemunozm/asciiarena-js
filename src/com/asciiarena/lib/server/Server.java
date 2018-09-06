package com.asciiarena.lib.server;

import java.io.IOException;
import java.net.ServerSocket;
import java.net.Socket;

import com.asciiarena.lib.common.communication.Connection;
import com.asciiarena.lib.common.communication.ConnectionError;
import com.asciiarena.lib.common.communication.Message;
import com.asciiarena.lib.common.logging.Log;
import com.asciiarena.lib.common.version.Version;

public class Server
{
    private final int port;
    private GameManager gameManager;

    public Server(ServerConfig config)
    {
        this.port = config.port;
        this.gameManager = new GameManager(config.game);
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
            Log.error("Can not open the server or port %d, port");
        }
    }

    private void clientConnection(Socket socket)
    {
        try
        {
            Connection connection = new Connection(socket);

            if(!checkVersion(connection))
            {
                connection.close();
                return;
            }

            if(!checkServerInfo(connection))
            {
                connection.close();
                return;
            }

            if(!gameManager.login(connection))
            {
                connection.close();
                return;
            }
        }
        catch(ConnectionError e)
        {
            Log.warning("Client connection error");
            return;
        }

        if(gameManager.getPlayerRegistry().isComplete())
        {
            gameManager.startGame();
            gameManager.reset();
        }
    }

    private boolean checkVersion(Connection connection) throws ConnectionError
    {
        Message.Version versionMessage = (Message.Version) connection.receive();

        Message.CheckedVersion checkedVersionMessage = new Message.CheckedVersion();
        checkedVersionMessage.version = Version.CURRENT;
        checkedVersionMessage.validation = validateVersion(versionMessage.version);
        connection.send(checkedVersionMessage);

        return checkedVersionMessage.validation;
    }

    private boolean checkServerInfo(Connection connection) throws ConnectionError
    {
        Message.ServerInfo serverInfoMessage = new Message.ServerInfo();
        serverInfoMessage.players = gameManager.getPlayerRegistry().getCharacters();
        serverInfoMessage.maxPlayers = gameManager.getPlayerRegistry().getMaxPlayers();
        serverInfoMessage.pointsToWin = gameManager.getPlayerRegistry().getPointsToWin();
        connection.send(serverInfoMessage);

        return !gameManager.getPlayerRegistry().isComplete();
    }

    private static boolean validateVersion(String version)
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

    public int getPort()
    {
        return port;
    }

    public GameManager getGameManager()
    {
        return gameManager;
    }

}
