package com.asciiarena.lib.server.match;

import com.asciiarena.lib.common.match.Wall;
import com.asciiarena.lib.common.util.Vector2;

public class Map
{
    private int width;
    private int height;
    private String seed;
    private Wall[][] grid;

    public Map(int width, int height, String seed)
    {
        this.width = width;
        this.height = height;
        this.seed = seed;
        this.grid = new Wall[width][height];

        clear();
        buildBorder();
        generate(seed.hashCode());
    }

    public void clear()
    {
        for(int y = 0; y < height; y++)
        {
            for(int x = 0; x < width; x++)
            {
                grid[x][y] = Wall.EMPTY;
            }
        }
    }

    private void buildBorder()
    {
        for(int x = 0; x < width; x++) 
        {
            grid[x][0] = Wall.BORDER;
        }

        for(int x = 0; x < width; x++) 
        {
            grid[x][height - 1] = Wall.BORDER;
        }

        for(int y = 1; y < height - 1; y++) 
        {
            grid[0][y] = Wall.BORDER;
        }

        for(int y = 1; y < height; y++) 
        {
            grid[width - 1][y] = Wall.BORDER;
        }
    }

    private void generate(int randomSeed)
    {
        //TODO
    }

    public void setPlace(Vector2 position, Wall wall)
    {
        grid[position.x][position.y] = wall;
    }

    public Wall getPlace(Vector2 position)
    {
        return grid[position.x][position.y];
    }

    public int getWidth()
    {
        return width;
    }

    public int getHeight()
    {
        return height;
    }

    public  String getSeed()
    {
        return seed;
    }

    public Wall[][] getGrid()
    {
        return grid;
    }
}
