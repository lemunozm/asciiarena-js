package main.java.server;

import java.io.IOException;
import java.net.ServerSocket;

import main.java.common.communication.Connection;
import main.java.common.communication.Message;

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
            @SuppressWarnings("resource")
            ServerSocket serverSocket = new ServerSocket(this.port);
            while (true) 
            {
                Connection connection = new Connection(serverSocket.accept());
                handleVersionRequest(connection);
            } 
        } 
        catch (IOException e)
        {
            e.printStackTrace();
        }
    }

    private boolean handleVersionRequest(Connection connection) 
    {
        Message.Version versionMessage = (Message.Version) connection.received();
        System.out.println(versionMessage.version);
        return false;
    }
}
