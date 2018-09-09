package com.asciiarena.lib.common.match;

import java.io.Serializable;

import com.asciiarena.lib.common.util.Vector2;

public class Entity implements Serializable
{
    private static final long serialVersionUID = 8794113723970536836L;

    private char character;
    private Vector2 position;
    private Direction direction;

    public Entity(char character)
    {
        this.character = character;
        this.position = new Vector2(-1, -1);
        this.direction = Direction.NONE;
    }

    public void setPosition(Vector2 position)
    {
        this.position.set(position);
    }

    public void move(Vector2 movement)
    {
        position.add(movement);
    }

    public void setDirection(Direction direction)
    {
        this.direction = direction;
    }

    public char getCharacter()
    {
        return character;
    }

    public Vector2 getPosition()
    {
        return position.clone();
    }

    public Direction Direction()
    {
        return direction;
    }
}
