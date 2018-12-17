package com.asciiarena.lib.client;

import com.asciiarena.lib.client.gui.terminal.Brush;
import com.asciiarena.lib.client.gui.terminal.Key;
import com.asciiarena.lib.client.gui.terminal.TerminalWindow;
import com.asciiarena.lib.common.communication.Connection;
import com.asciiarena.lib.common.communication.ConnectionError;

public class Game
{
    private TerminalWindow terminal;
    private Brush screen;
    private int width;
    private int height;

    public Game(int width, int height)
    {
        this.terminal = new TerminalWindow("AsciiArena", width * 2 - 1, height);
        this.screen = terminal.createBrush();
        //init point register
        this.width = width;
        this.height = height;
    }

    public void run(Connection connection) throws ConnectionError
    {
        System.out.println("Initializing game...");
        while(true) //points
        {
            Match match = new Match(width, height, screen);
            match.init(connection);
            terminal.show();

            //wait 3 seconds here
            while(true) //while is more than one alive
            {
                match.update(connection);
                //Save and update player information (points)
                //check if match finished
                match.playerAction(connection, readUserAction());
                terminal.show();
            }
        }

        //terminal.close();
        //Prints the winner and the points here in the console
        //System.out.println("Finish game...");
    }

    private PlayerAction readUserAction()
    {
        if(terminal.isKeyDown(Key.UP) || terminal.isKeyDown(Key.K) || terminal.isKeyDown(Key.W))
        {
            return new PlayerAction(PlayerAction.Movement.UP);
        }
        else if(terminal.isKeyDown(Key.RIGHT) || terminal.isKeyDown(Key.L) || terminal.isKeyDown(Key.D))
        {
            return new PlayerAction(PlayerAction.Movement.RIGHT);
        }
        else if(terminal.isKeyDown(Key.DOWN) || terminal.isKeyDown(Key.J) || terminal.isKeyDown(Key.S))
        {
            return new PlayerAction(PlayerAction.Movement.DOWN);
        }
        else if(terminal.isKeyDown(Key.LEFT) || terminal.isKeyDown(Key.H) || terminal.isKeyDown(Key.A))
        {
            return new PlayerAction(PlayerAction.Movement.LEFT);
        }
        else
        {
            return new PlayerAction(PlayerAction.Movement.NONE);
        }
    }
}
