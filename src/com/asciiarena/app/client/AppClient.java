package com.asciiarena.app.client;

import java.io.IOException;
import java.net.Socket;

import com.asciiarena.lib.common.communication.Connection;
import com.asciiarena.lib.common.communication.Message;
import com.asciiarena.lib.common.logging.Log;

public class AppClient
{
    public static void main(String[] args) 
    {
        Log.init();
        try
        {
            Socket socket = new Socket("127.0.0.1", 3000);
            Connection connection = new Connection(socket);

            Message.Version versionMessage = new Message.Version("1.0.0");
            connection.send(versionMessage);

            Message.CheckedVersion checkedVersionMessage = (Message.CheckedVersion) connection.receive();
            if(checkedVersionMessage.validation)
            {
                Message.ServerInfo serverInfoMessage = (Message.ServerInfo) connection.receive();
                login(serverInfoMessage.port, args[0].charAt(0));
            }
        } 
        catch (IOException e)
        {
            e.printStackTrace();
        }    
    }

    public static void login(int port, char character)
    {
        try
        {
            Socket socket = new Socket("127.0.0.1", 3001);
            Connection connection = new Connection(socket);

            Message.NewPlayer newPlayerMessage = new Message.NewPlayer(character);
            connection.send(newPlayerMessage);

            Message.PlayerLogin playerLoginMessage = (Message.PlayerLogin) connection.receive(); 
            if(playerLoginMessage.status == Message.PlayerLogin.Status.SUCCESSFUL)
            {
                int currentPlayers;
                do
                {
                    Message.PlayersInfo playersLoginMessage = (Message.PlayersInfo) connection.receive(); 
                    currentPlayers = playersLoginMessage.characters.size();
                }
                while(currentPlayers < playerLoginMessage.maxPlayers);
            }
        }
        catch (IOException e)
        {
            e.printStackTrace();
        }
    }
}
