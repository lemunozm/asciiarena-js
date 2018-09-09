package com.asciiarena.lib.client.gui.terminal;

import java.awt.Color;

public class Tile
{
    public static final char NONE = '\0';

    private char character;
    private Color background;
    private Color foreground;

    public Tile(char character)
    {
        this(character, null, null);
    }

    public Tile(char character, Color foreground)
    {
        this(character, foreground, null);
    }

    public Tile(char character, Color foreground, Color background)
    {
        this.character = character;
        this.foreground = foreground;
        this.background = background;
    }

    public void set(char character, Color foreground, Color background)
    {
        this.character = character;
        this.foreground = foreground;
        this.background = background;
    }

    public void clear()
    {
        set(NONE, null, null);
    }

    public void setCharacter(char character)
    {
        this.character = character;
    }

    public void setBackground(Color background)
    {
        this.background = background;
    }

    public void setForeground(Color foreground)
    {
        this.foreground = foreground;
    }

    public char getCharacter()
    {
        return character;
    }

    public Color getForeground()
    {
        return foreground;
    }

    public Color getBackground()
    {
        return background;
    }
}
