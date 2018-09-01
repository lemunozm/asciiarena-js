package com.asciiarena.lib.server;

import java.io.IOException;
import java.net.ServerSocket;

import com.asciiarena.lib.common.communication.Connection;
import com.asciiarena.lib.common.communication.Message;
import com.asciiarena.lib.common.logging.Log;
import com.asciiarena.lib.common.version.Version;

public class InfoServer
{
    private GameServer gameServer;
    private int port;

    public InfoServer(ServerConfig.InfoConfig config, GameServer gameServer)
    {
        this.port = config.port;
        this.gameServer = gameServer;
    }

    public void listen()
    {
        try(ServerSocket serverSocket = new ServerSocket(port))
        {
            while (true) 
            {
                Connection connection = new Connection(serverSocket.accept());
                infoRequest(connection);
            } 
        }
        catch (IOException e)
        {
            e.printStackTrace();
        }
    }

    private void infoRequest(Connection connection) 
    {
        if(checkVersion(connection))
        {
            sendServerInfo(connection);
        }
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
        serverInfoMessage.port = gameServer.getPort();
        serverInfoMessage.currentPlayers = gameServer.getGameManager().getPlayerRegistry().getCurrentPlayers();
        serverInfoMessage.maxPlayers = gameServer.getGameManager().getPlayerRegistry().getMaxPlayers();
        connection.send(serverInfoMessage);
    }
}
