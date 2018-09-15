package com.asciiarena.lib.server.player;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

import com.asciiarena.lib.common.communication.Connection;
import com.asciiarena.lib.common.communication.ConnectionError;

import javafx.util.Pair;

public class PlayerRegistry
{
    public static enum Status
    {
        OK, 
        FULL, 
        ALREADY_EXISTS;
    }

    private ArrayList<Player> players;
    private final int maxPlayers;
    private final int pointsToWin;

    public PlayerRegistry(int maxPlayers, int pointsToWin)
    {
        this.players = new ArrayList<Player>(maxPlayers);
        this.maxPlayers = maxPlayers;
        this.pointsToWin = pointsToWin;
    }

    public Status add(char character, Connection connection)
    {
        if(players.size() == maxPlayers)
        {
            return Status.FULL;
        }

        for(Player player: players)
        {
            if(player.getCharacter()== character)
            {
                return Status.ALREADY_EXISTS;
            }
        }

        players.add(new Player(character, connection));

        return Status.OK;
    }        

    public void sendToPlayers(Object message) 
    {
        for(Player player: players)
        {
            try
            {
                if(player.isConnected())
                {
                    player.getConnection().send(message);
                }
            }
            catch (ConnectionError e)
            {
                player.markAsDisconnected();
            }
        }
    }

    public List<Pair<Player, Object>> receiveFromPlayers() 
    {
        ArrayList<Pair<Player, Object>> messages = new ArrayList<Pair<Player, Object>>(players.size());
        for(Player player: players)
        {
            try
            {
                Object message = null;
                if(player.isConnected())
                {
                    message = player.getConnection().receive(); 
                }
                messages.add(new Pair<Player, Object>(player, message));
            }
            catch (ConnectionError e)
            {
                player.markAsDisconnected();
            }
        }
        return messages; 
    }

    public boolean hasWinner()
    {
        for(Player player: players)
        {
            if(player.getPoints() >= pointsToWin)
            {
                return true;
            }
        }

        return false;
    }

    public boolean isComplete()
    {
        return players.size() == maxPlayers;
    }

    public List<Character> getCharacters()
    {
        ArrayList<Character> characters = new ArrayList<Character>(players.size());

        for(Player player: players)
        {
            characters.add(player.getCharacter());
        }

        return characters;
    }

    public List<Player> getPlayers()
    {
        return Collections.unmodifiableList(players);
    }

    public int getCurrentPlayers()
    {
        return players.size();
    }

    public int getMaxPlayers()
    {
        return maxPlayers;
    }

    public int getPointsToWin()
    {
        return pointsToWin;
    }
}
