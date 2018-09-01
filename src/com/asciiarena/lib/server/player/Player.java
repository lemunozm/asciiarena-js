package com.asciiarena.lib.server.player;

import com.asciiarena.lib.common.communication.Connection;

public class Player
{
    private char character;
    private Connection connection;
    private int points;

    public Player(char character, Connection connection)
    {
        this.character = character;
        this.connection = connection;
    }

    public void addPoints(int points)
    {
        this.points += points; 
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
