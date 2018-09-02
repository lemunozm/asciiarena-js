package com.asciiarena.lib.server.player;

import java.util.ArrayList;
import java.util.Collections;
import java.util.Iterator;
import java.util.List;

import com.asciiarena.lib.common.communication.Connection;

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

        for(Iterator<Player> it = players.iterator(); it.hasNext();)
        {
            if(it.next().getCharacter()== character)
            {
                return Status.ALREADY_EXISTS;
            }
        }

        players.add(new Player(character, connection));

        return Status.OK;
    }        

    public boolean sendToPlayers(Object object) 
    {
        boolean sendStatus = true;
        for(Iterator<Player> it = players.iterator(); it.hasNext();)
        {
            sendStatus &= it.next().getConnection().send(object);
        }

        return sendStatus;
    }

    public List<Object> receiveFromPlayers() 
    {
        ArrayList<Object> objects = new ArrayList<Object>(players.size());
        for(Iterator<Player> it = players.iterator(); it.hasNext();)
        {
            objects.add(it.next().getConnection().receive());
        }

        return objects; 
    }

    public boolean hasWinner()
    {
        for(Iterator<Player> it = players.iterator(); it.hasNext();)
        {
            if(it.next().getPoints() >= pointsToWin)
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

        for(Iterator<Player> it = players.iterator(); it.hasNext();)
        {
            characters.add(it.next().getCharacter());
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
}
