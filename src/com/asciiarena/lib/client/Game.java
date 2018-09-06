package com.asciiarena.lib.client;

import com.asciiarena.lib.common.communication.Connection;
import com.asciiarena.lib.common.communication.ConnectionError;
import com.asciiarena.lib.common.communication.Message;
import com.asciiarena.lib.common.match.Entity;
import com.asciiarena.lib.common.match.Wall;
import com.asciiarena.lib.common.util.Vector2;

public class Game
{
    private Connection connection;

    public Game(Connection connection)
    {
        this.connection = connection;
    }

    public void start() throws ConnectionError
    {
        //init point register
        //init screen
        System.out.println("Initializing game...");
        
        //while
            Message.MatchInfo matchInfoMessage = (Message.MatchInfo) connection.receive();
            for(int y = 0; y < matchInfoMessage.height; y++)
            {
                for(int x = 0; x < matchInfoMessage.width; x++)
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
                    System.out.printf("%c ", (character != '\0') ? character : mapGraphic); 
                }
                System.out.printf("\n");
            }

            Match match = new Match();

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
