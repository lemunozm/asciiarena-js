package com.asciiarena.lib.server.player;

import com.asciiarena.lib.common.communication.Connection;

public class Player
{
    private char character;
    private Connection connection;
    private boolean connectionLost;
    private int points;

    public Player(char character, Connection connection)
    {
        this.character = character;
        this.connection = connection;
        this.connectionLost = false;
    }

    public void addPoints(int points)
    {
        this.points += points; 
    }

    void markAsDisconnected()
    {
        connectionLost = true;
    }

    boolean isConnected()
    {
        return connectionLost;
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
