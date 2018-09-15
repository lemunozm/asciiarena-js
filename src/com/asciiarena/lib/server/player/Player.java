package com.asciiarena.lib.server.player;

import com.asciiarena.lib.common.communication.Connection;
import com.asciiarena.lib.common.logging.Log;

public class Player
{
    private char character;
    private Connection connection;
    private boolean connected;
    private int points;

    public Player(char character, Connection connection)
    {
        this.character = character;
        this.connection = connection;
        this.connected = true;
    }

    public void addPoints(int points)
    {
        this.points += points; 
    }

    public void markAsDisconnected()
    {
        Log.warning("Player %c disconnected", character);
        connected = false;
    }

    public boolean isConnected()
    {
        return connected;
    }

    public char getCharacter()
    {
        return character;
    }

    public Connection getConnection()
    {
        return connection;
    }

    public int getPoints()
    {
        return points;
    }
}
