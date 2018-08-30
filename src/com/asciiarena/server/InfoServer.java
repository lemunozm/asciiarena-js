package com.asciiarena.server;

import java.io.IOException;
import java.net.ServerSocket;

import com.asciiarena.common.communication.Connection;
import com.asciiarena.common.communication.Message;
import com.asciiarena.common.logging.Log;
import com.asciiarena.common.version.Version;

public class InfoServer
{
    //private GameServer gameSever;
    private int port;

    public InfoServer(ServerConfig.InfoConfig config, GameServer gameServer)
    {
        this.port = config.port;
        //this.gameSever = gameServer;
    }

    public void run()
    {
        try
        {
            try(ServerSocket serverSocket = new ServerSocket(this.port))
            {
                while (true) 
                {
                    Connection connection = new Connection(serverSocket.accept());
                    handleVersionRequest(connection);
                } 
            }
        } 
        catch (IOException e)
        {
            e.printStackTrace();
        }
    }

    private boolean handleVersionRequest(Connection connection) 
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
                Log.warning("Compatible versions, but are not the same: client is %s and server is %s", version, Version.CURRENT);
                return true;
            case ERROR:
                Log.error("Incompatible versions: client is %s and server is %s", version, Version.CURRENT);
            default:
                return false;
        }
    }
}
