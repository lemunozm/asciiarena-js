package com.asciiarena.lib.client;

import java.io.IOException;
import java.net.Socket;
import java.util.List;

import com.asciiarena.lib.common.communication.Connection;
import com.asciiarena.lib.common.communication.ConnectionError;
import com.asciiarena.lib.common.communication.Message;
import com.asciiarena.lib.common.version.Version;

public class Client
{
    public static final char ASK_FOR_CHARACTER = '\0';
    private String ip;
    private int port;
    private char character;
    private List<Character> players;
    private int maxPlayers;

    public Client(String ip, int port, char character)
    {
        this.ip = ip;
        this.port = port;
        this.character = character;
    }

    public void start()
    {
        try
        {
            Connection connection = new Connection(new Socket(ip, port));

            if(!checkServerToPlay(connection)) 
            {
                connection.close();
                return;
            }

            if(!login(connection))
            {
                connection.close();
                return;
            }

            Game game = new Game(connection);
            game.start();
        } 
        catch (ConnectionError e)
        {
            System.err.printf("Error: Connection lost\n");
            System.exit(1);
        }
        catch (IOException e)
        {
            System.err.printf("Server connection error. ip: %s, port: %d\n", ip, port);
            System.exit(1);
        }
    }

    private boolean checkServerToPlay(Connection connection) throws ConnectionError
    {
        Message.Version versionMessage = new Message.Version(Version.CURRENT);
        connection.send(versionMessage);

        Message.CheckedVersion checkedVersionMessage = (Message.CheckedVersion) connection.receive();
        System.out.printf("Client version: %s - Server version: %s\n", Version.CURRENT, checkedVersionMessage.version);

        if(checkedVersionMessage.validation)
        {
            Message.ServerInfo serverInfoMessage = (Message.ServerInfo) connection.receive();
            players = serverInfoMessage.players;
            maxPlayers = serverInfoMessage.maxPlayers;

            System.out.printf(getServerGameStateMessage());
            if(players.size() ==  maxPlayers)
            {
                System.out.printf("The game is already started\n");
            }

            return players.size() < maxPlayers;
        }

        return false; 
    }

    private boolean login(Connection connection) throws ConnectionError
    {
        if(character == ASK_FOR_CHARACTER || players.contains(character))
        {
            character = askForCharacter();
        }

        Message.NewPlayer newPlayerMessage = new Message.NewPlayer(character);
        connection.send(newPlayerMessage);

        Message.PlayerLogin playerLoginMessage = (Message.PlayerLogin) connection.receive(); 
        switch(playerLoginMessage.status)
        {
            case SUCCESSFUL:
                do
                {
                    Message.PlayersInfo playersLoginMessage = (Message.PlayersInfo) connection.receive(); 
                    players = playersLoginMessage.players;
                    System.out.printf(getServerGameStateMessage());
                }
                while(players.size() < maxPlayers);
                return true; 

            case CHARACTER_ALREADY_EXISTS:
                System.out.printf("Sorry, character '%c' already exists in the server");
                return false;

            case GAME_COMPLETE:
                System.out.printf("Sorry, Game is complete");
                return false;

            default:
                return false;
        }
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

    private String getServerGameStateMessage()
    {
        String state = (players.size() < maxPlayers) ? "Waiting for players..." : "Complete!";
        return String.format("%s %d/%d %s\n", state, players.size(), maxPlayers, players);
    }
}
