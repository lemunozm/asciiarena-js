package com.asciiarena.lib.server.match;

import java.util.ArrayList;
import java.util.List;
import java.util.Random;

import com.asciiarena.lib.common.match.Entity;
import com.asciiarena.lib.common.match.Wall;
import com.asciiarena.lib.common.util.Vector2;

public class Match
{
    private Map map;
    private ArrayList<Entity> entities;

    public Match(int width, int height, String seed, List<Character> characters)
    {
        this.map = new Map(width, height, seed);
        this.entities = new ArrayList<Entity>();

        int minEntityDistance = (int) (Math.sqrt((width * height) / characters.size()) / 2);
        for(Character character: characters)
        {
            Entity entity = new Entity(character);
            entity.setPosition(searchEmptyRandomPosition(minEntityDistance));

            entities.add(entity); 
        }
    }

    public void update(List<EntityAction> entityActions)
    {
        for(EntityAction action: entityActions)
        {
            if(action.getMovement() != null)
            {
                Vector2 movement = action.getMovement().getVector();
                Vector2 entityPosition = action.getEntity().getPosition();

                Vector2 futurePosition = entityPosition.add(movement);
                if(map.getPlace(futurePosition) == Wall.EMPTY && !existEntity(futurePosition))
                {
                    action.getEntity().move(movement);
                }
            }
        }
    }

    public Vector2 searchEmptyRandomPosition(int minEntityDistance)
    {
        ArrayList<Vector2> emptyPlaces = new ArrayList<Vector2>(map.getWidth() * map.getHeight()); 
        for(int y = 0; y < map.getHeight(); y++)
        {
            for(int x = 0; x < map.getWidth(); x++)
            {
                Vector2 position = new Vector2(x, y);
                if(map.getPlace(position) == Wall.EMPTY && getClosedEntityDistance(position) > minEntityDistance) 
                {
                    emptyPlaces.add(position);
                }
            }
        }
        
        return emptyPlaces.get(new Random().nextInt(emptyPlaces.size()));
    }

    public int getClosedEntityDistance(Vector2 position)
    {
        int minDistance = Integer.MAX_VALUE;
        for(Entity entity: entities)
        {
            int distance = entity.getPosition().getDistanceTo(position);
            if(distance < minDistance)
            {
                minDistance = distance;
            }
        }

        return minDistance;
    }

    public boolean existEntity(Vector2 position)
    {
        for(Entity entity: entities)
        {
            if(position.equals(entity.getPosition()))
            {
                return true;
            }
        }

        return false;
    }

    public Entity getEntity(char character)
    {
        for(Entity entity: entities)
        {
            if(entity.getCharacter() == character)
            {
                return entity;
            }
        }

        return null;
    }

    public boolean hasFinished()
    {
        //TODO
        return false;   
    }

    public Map getMap()
    {
        return map;
    }

    public List<Entity> getEntities()
    {
        return entities;
    }
}
