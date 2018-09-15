package com.asciiarena.lib.client;

import java.util.List;

import com.asciiarena.lib.client.gui.terminal.Brush;
import com.asciiarena.lib.client.gui.terminal.Tile;
import com.asciiarena.lib.common.communication.Connection;
import com.asciiarena.lib.common.communication.ConnectionError;
import com.asciiarena.lib.common.communication.Message;
import com.asciiarena.lib.common.match.Direction;
import com.asciiarena.lib.common.match.Entity;
import com.asciiarena.lib.common.match.MatchSynchronization;
import com.asciiarena.lib.common.match.Wall;
import com.asciiarena.lib.common.util.Vector2;

public class Match
{
    private Brush screen;
    private Wall[][] mapGrid;
    private List<Entity> entities;
    private int width;
    private int height;
    private MatchSynchronization matchSynchronization;

    public Match(int width, int height, Brush matchScreen)
    {
        this.screen = matchScreen;
        this.mapGrid = null;
        this.entities = null;
        this.width = width;
        this.height = height;
        this.matchSynchronization = new MatchSynchronization();
    }

    public void init(Connection connection) throws ConnectionError
    {
        Message.MatchInfo matchInfoMessage = (Message.MatchInfo) connection.receive();
        mapGrid = matchInfoMessage.grid;
        entities = matchInfoMessage.entities;
    }

    public void update(Connection connection) throws ConnectionError
    {
        matchSynchronization.waitForNextFrame();

        Message.Frame frameMessage = (Message.Frame) connection.receive();
        entities = frameMessage.entities;
    }

    public void playerAction(Connection connection, PlayerAction action) throws ConnectionError
    {
        Message.PlayerAction playerActionMessage = new Message.PlayerAction();
        switch(action.getMovement())
        {
            case UP:
                playerActionMessage.movement = Direction.UP;
                break;
            case RIGHT:
                playerActionMessage.movement = Direction.RIGHT;
                break;
            case DOWN:
                playerActionMessage.movement = Direction.DOWN;
                break;
            case LEFT:
                playerActionMessage.movement = Direction.LEFT;
                break;
            case NONE:
            default:
                return;
        }
        connection.send(playerActionMessage);
    }

    public void render()
    {
        for(int y = 0; y < height; y++)
        {
            for(int x = 0; x < width; x++)
            {
                char mapGraphic = (mapGrid[x][y] == Wall.BORDER) ? 'X' : ' ';
                char character = '\0';
                for(Entity entity: entities)
                {
                    if(entity.getPosition().equals(new Vector2(x, y)))
                    {
                        character = entity.getCharacter(); 
                        break;
                    }
                }
                screen.draw(x * 2, y, new Tile((character != '\0') ? character : mapGraphic));
            }
        }
    }
}
