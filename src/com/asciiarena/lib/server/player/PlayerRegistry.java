package com.asciiarena.lib.server.player;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

import com.asciiarena.lib.common.communication.Connection;
import com.asciiarena.lib.common.communication.ConnectionError;
import com.asciiarena.lib.common.logging.Log;

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

    public void sendToPlayers(Object object) 
    {
        for(Player player: players)
        {
            try
            {
                if(!player.isConnected())
                {
                    player.getConnection().send(object);
                }
            }
            catch (ConnectionError e)
            {
                player.markAsDisconnected();
                Log.warning("Player %c disconnected", player.getCharacter());
            }
        }
    }

    public List<Object> receiveFromPlayers() 
    {
        ArrayList<Object> objects = new ArrayList<Object>(players.size());
        for(int i = 0; i < players.size(); i++)
        {
            try
            {
                if(!players.get(i).isConnected())
                {
                    objects.set(i, players.get(i).getConnection().receive());
                }
            }
            catch (ConnectionError e)
            {
                players.get(i).markAsDisconnected();
                Log.warning("Player %c disconnected", players.get(i).getCharacter());
            }
        }
        return objects; 
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
