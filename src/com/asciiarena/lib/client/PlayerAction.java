package com.asciiarena.lib.client;

public class PlayerAction
{
    public static enum Movement
    {
        UP, RIGHT, DOWN, LEFT, NONE;
    }

    private Movement movement;
    //private SkillID or something

    public PlayerAction(Movement movement)
    {
        this.movement = movement;
    }

    public Movement getMovement()
    {
        return movement;
    }
}
