package com.asciiarena.lib.server.event;

import com.asciiarena.lib.common.match.Direction;

public class MovementEvent
{
    private static final int DEFAULT_MOVEMENT_COOLDOWN = 5;

    private Direction movement = null;
    private int cooldown = 0;

    public MovementEvent()
    {
        this.movement = null;
        this.cooldown = 0;
    }

    public void setMovement(Direction movement)
    {
        if(cooldown == 0)
        {
            this.movement = movement;
        }
    }

    public Direction requestMovement()
    {
        if(cooldown == 0)
        {
            Direction validMovement = movement; 
            if(movement != null)
            {
                movement = null;
                cooldown = DEFAULT_MOVEMENT_COOLDOWN;
            }
            return validMovement;
        }

        if(cooldown > 0)
        {
            cooldown -= 1;
        }

        return null;
    }
}
