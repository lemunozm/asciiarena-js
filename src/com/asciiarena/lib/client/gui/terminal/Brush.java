package com.asciiarena.lib.client.gui.terminal;

import java.awt.Color;

public class Brush
{
    private Tile[][] tiles;
    private int originX;
    private int originY;
    private int width;
    private int height;
    private Color defaultForeground;
    private Color defaultBackground;

    Brush(Tile[][] tiles, int x, int y, int width, int height)
    {
        this.tiles = tiles;
        this.originX = x;
        this.originY = y;
        this.width = width;
        this.height = height;
        this.defaultForeground = null;
        this.defaultBackground = null;
    }

    public void selectForeground(Color color)
    {
        defaultBackground = color;
    }

    public void selectBackground(Color color)
    {
        defaultBackground = color;
    }
    
    public void clear()
    {
        fill(new Tile(Tile.NONE, defaultForeground, defaultBackground));
    }

    public void fill(Tile tile)
    {
        fill(originX, originY, width, height, tile);
    }

    public void fill(int fromX, int fromY, int width, int height, Tile tile)
    {
        if(fromX + width < this.width && fromY + height < this.height)
        {
            for(int y = fromY; y < height; y++)
            {
                for(int x = fromX; x < width; x++)
                {
                    stampTile(tiles[originX + x][originY + y], tile);
                }
            }
        }
        else
        {
            try
            {
                throw new TerminalException("Drawing out of the brush frame.");
            }
            catch (TerminalException e)
            {
                e.printStackTrace();
            }
        }
    }

    public void draw(int x, int y, Tile tile)
    {
        if(x < width && y < height)
        {
            stampTile(tiles[originX + x][originY + y], tile);
        }
        else
        {
            try
            {
                throw new TerminalException("Drawing out of the brush frame. Position: " + x + ", " + y + ".");
            }
            catch (TerminalException e)
            {
                e.printStackTrace();
            }
        }
    }

    private void stampTile(Tile to, Tile from)
    {
        to.setCharacter(from.getCharacter());

        if(from.getForeground() != null)
        {
            to.setForeground(from.getForeground());
        }
        else if(defaultForeground != null)
        {
            to.setForeground(defaultForeground);
        }

        if(from.getBackground() != null)
        {
            to.setBackground(from.getBackground());
        }
        else if(defaultBackground != null)
        {
            to.setBackground(defaultBackground);
        }
    }

    public int getOriginX()
    {
        return originX;
    }

    public int getOriginY()
    {
        return originY;
    }

    public int getWidth()
    {
        return width;
    }

    public int getHeight()
    {
        return height;
    }

    public Color getDefaultForeground()
    {
        return defaultForeground;
    }

    public Color getDefaultBackground()
    {
        return defaultBackground;
    }
}
