package com.asciiarena.lib.client;

import com.asciiarena.lib.client.gui.terminal.Brush;
import com.asciiarena.lib.client.gui.terminal.TerminalWindow;
import com.asciiarena.lib.client.gui.terminal.Tile;
import com.asciiarena.lib.common.communication.Connection;
import com.asciiarena.lib.common.communication.ConnectionError;
import com.asciiarena.lib.common.communication.Message;
import com.asciiarena.lib.common.match.Entity;
import com.asciiarena.lib.common.match.Wall;
import com.asciiarena.lib.common.util.Vector2;

public class Game
{
    private Connection connection;
    private int width;
    private int height;

    public Game(Connection connection, int width, int height)
    {
        this.connection = connection;
        this.width = width;
        this.height = height;
    }

    public void start() throws ConnectionError
    {
        System.out.println("Initializing game...");
        //init point register
        TerminalWindow term = new TerminalWindow("AsciiArena", width * 2 - 1, height);
        Brush screen = term.createBrush();
        //while
            Message.MatchInfo matchInfoMessage = (Message.MatchInfo) connection.receive();
            for(int y = 0; y < height; y++)
            {
                for(int x = 0; x < width; x++)
                {
                    char mapGraphic = (matchInfoMessage.grid[x][y] == Wall.BORDER) ? 'X' : ' ';
                    char character = '\0';
                    for(Entity entity: matchInfoMessage.entities)
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

            Match match = new Match();
            term.render();

            //while(more than one alive)
                //match.update(); ==> a reception wait here about 3 seconds at first loop.
                //render here
                    //private render()
                    //match.render

                //capture the event here (transform to movement and skill)
                //match.event(skill id, movement id );

            //Message: list of points of each player
            //Save and update player information (points)
        //close screen

        //Prints the winner and the points here
    }
}
