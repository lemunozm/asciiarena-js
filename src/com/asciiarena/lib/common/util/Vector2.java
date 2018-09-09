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

    public Vector2 set(int x, int y)
    {
        this.x = x;
        this.y = y;

        return this;
    }

    public Vector2 set(Vector2 v)
    {
        this.x = v.x;
        this.y = v.y;

        return this;
    }

    public Vector2 add(int x, int y)
    {
        this.x += x;
        this.y += y;

        return this;
    }

    public Vector2 add(Vector2 v)
    {
        x += v.x;
        y += v.y;

        return this;
    }

    public Vector2 sub(int x, int y)
    {
        this.x -= x;
        this.y -= y;

        return this;
    }

    public Vector2 sub(Vector2 v)
    {
        x -= v.x;
        y -= v.y;

        return this;
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
