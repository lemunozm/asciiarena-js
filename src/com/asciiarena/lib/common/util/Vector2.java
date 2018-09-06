package com.asciiarena.lib.common.util;

import java.io.Serializable;

public class Vector2 implements Serializable
{
    private static final long serialVersionUID = 823672896676157807L;

    public int x;
    public int y;

    public Vector2() 
    {
    }

    public Vector2(int x, int y)
    {
        this.x = x;
        this.y = y;
    }

    @Override
    public boolean equals(Object other)
    {
        if(other instanceof Vector2)
        {
            Vector2 v = (Vector2) other;
            return x == v.x && y == v.y;
        }

        return false;
    }

    @Override
    public Vector2 clone()
    {
        return new Vector2(x, y);
    }

    @Override
    public String toString()
    {
        return "(" + x + ", " + y + ")"; 
    }

    public void set(int x, int y)
    {
        this.x = x;
        this.y = y;
    }

    public void set(Vector2 v)
    {
        this.x = v.x;
        this.y = v.y;
    }

    public void add(int x, int y)
    {
        this.x += x;
        this.y += y;
    }

    public void add(Vector2 v)
    {
        x += v.x;
        y += v.y;
    }

    public void sub(int x, int y)
    {
        this.x -= x;
        this.y -= y;
    }

    public void sub(Vector2 v)
    {
        x -= v.x;
        y -= v.y;
    }

    public int getLength() 
    {
        return (int) Math.sqrt(x * x + y * y);
    }

    public int getDistanceTo(Vector2 v) 
    {
        int xDiff = x - v.x;
        int yDiff = y - v.y;
        return (int) Math.sqrt(xDiff * xDiff + yDiff * yDiff);
    }
}
