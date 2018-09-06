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

    public Vector2 searchEmptyRandomPosition(int minEntityDistance)
    {
        ArrayList<Vector2> emptyPlaces = new ArrayList<Vector2>(map.getWidth() * map.getHeight()); 
        for(int y = 0; y < map.getHeight(); y++)
        {
            for(int x = 0; x < map.getWidth(); x++)
            {
                Vector2 position = new Vector2(x, y);
                if(map.getPlace(position) == Wall.EMPTY) 
                {
                    boolean free = true; 
                    for(Entity entity: entities)
                    {
                        free &= entity.getPosition().getDistanceTo(position) > minEntityDistance;
                    }

                    if(free)
                    {
                        emptyPlaces.add(position);
                    }
                }
            }
        }
        
        return emptyPlaces.get(new Random().nextInt(emptyPlaces.size()));
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
