package com.asciiarena.lib.common.match;

import com.asciiarena.lib.common.util.Vector2;

public enum Direction
{
    NONE(new Vector2(0, 0)),
    UP(new Vector2(0, -1)),
    RIGHT(new Vector2(1, 0)),
    DOWN(new Vector2(0, 1)),
    LEFT(new Vector2(-1, 0));

    private Vector2 vector;

    Direction(Vector2 vector)
    {
        this.vector = vector;
    }

    public Vector2 getVector()
    {
        return vector;
    }
}
