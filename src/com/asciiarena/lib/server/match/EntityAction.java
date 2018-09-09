package com.asciiarena.lib.server.match;

import com.asciiarena.lib.common.match.Direction;
import com.asciiarena.lib.common.match.Entity;

public class EntityAction
{
    private Entity entity;
    //private Direction view;
    private Direction movement;
    //private Skill skill;

    public EntityAction(Entity entity, Direction movement)
    {
        this.entity = entity;
        this.movement = movement;
    }

    public Entity getEntity()
    {
        return entity;
    }

    public Direction getMovement()
    {
        return movement;
    }
}
