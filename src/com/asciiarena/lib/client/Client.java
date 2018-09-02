package com.asciiarena.lib.client;

import java.io.IOException;
import java.net.Socket;
import java.util.List;

import com.asciiarena.lib.common.communication.Connection;
import com.asciiarena.lib.common.communication.Message;
import com.asciiarena.lib.common.logging.Log;
import com.asciiarena.lib.common.version.Version;

public class Client
{
    private String ip;
    private int port;
    private char character;
    private List<Character> players;
    private int maxPlayers;

    public Client(String ip, int port)
    {
        Log.init();
        this.ip = ip;
        this.port = port;
    }

    public void start()
    {
        Connection connection = connect(ip, port);

        if(!checkServerToPlay(connection)) 
        {
            connection.close();
            return;
        }

        if(login(connection))
        {
            connection.close();
            return;
        }

        //startGame();
    }

    private boolean checkServerToPlay(Connection connection)
    {
        Message.Version versionMessage = new Message.Version(Version.CURRENT);
        connection.send(versionMessage);

        Message.CheckedVersion checkedVersionMessage = (Message.CheckedVersion) connection.receive();
        System.out.printf("Client version: %s. Server version: %s\n", Version.CURRENT, checkedVersionMessage.version);

        if(checkedVersionMessage.validation)
        {
            Message.ServerInfo serverInfoMessage = (Message.ServerInfo) connection.receive();
            players = serverInfoMessage.players;
            maxPlayers = serverInfoMessage.maxPlayers;

            System.out.printf(getServerGameStateMessage());

            return players.size() < maxPlayers;
        }

        return false; 
    }

    private boolean login(Connection connection)
    {
        if(character == '\0' || players.contains(character))
        {
            character = askForCharacter();
        }

        Message.NewPlayer newPlayerMessage = new Message.NewPlayer(character);
        connection.send(newPlayerMessage);

        Message.PlayerLogin playerLoginMessage = (Message.PlayerLogin) connection.receive(); 
        if(playerLoginMessage.logged)
        {
            do
            {
                Message.PlayersInfo playersLoginMessage = (Message.PlayersInfo) connection.receive(); 
                players = playersLoginMessage.players;
                System.out.printf(getServerGameStateMessage());
            }
            while(players.size() < maxPlayers);
        }

        return playerLoginMessage.logged; 
    }

    private char askForCharacter()
    {
        char inputCharacter = '\0';
        while(!Character.isUpperCase(inputCharacter))
        {
            System.out.printf("Choose a player (only characters from A to Z are allowed)\n");
            System.out.printf("Player: ");
            try
            {
                inputCharacter = (char) System.in.read();
            } 
            catch (IOException e)
            {
                e.printStackTrace();
            }
        }
        return inputCharacter;
    }

    private Connection connect(String ip, int port)
    {
        try
        {
            Socket socket = new Socket(ip, port);
            return new Connection(socket);
        } 
        catch (IOException e)
        {
            System.err.printf("Connection error with ip: %s, port: %d\n", ip, port);
            System.exit(1);
        }     

        return null;
    }

    private String getServerGameStateMessage()
    {
        String state = (players.size() < maxPlayers) ? "Waiting for players" : "Game complete";
        return String.format("%s: %d/%d %s\n", state, players.size(), maxPlayers, players);
    }

    public void setDefaultCharacter(char character)
    {
        this.character = character;
    }
}
