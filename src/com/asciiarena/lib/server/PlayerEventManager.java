package com.asciiarena.lib.server;

import com.asciiarena.lib.common.communication.ConnectionError;
import com.asciiarena.lib.common.communication.Message;
import com.asciiarena.lib.common.match.Direction;
import com.asciiarena.lib.server.event.MovementEvent;
import com.asciiarena.lib.server.player.Player;

public class PlayerEventManager
{
    private Player player;
    private MovementEvent movementEvent;

    public PlayerEventManager(Player player)
    {
        this.player = player;
        this.movementEvent = new MovementEvent();

        Runnable listenEventRun = new Runnable() 
        {
            @Override
            public void run() 
            {
                listenEvent();
            }
        };  

        new Thread(listenEventRun).start(); //Manage this as class attribute? Add a close function
    }

    private void listenEvent()
    {
        while(player.isConnected())
        {
            try
            {
                Message.PlayerAction actionMessage = (Message.PlayerAction) player.getConnection().receive();
                movementEvent.setMovement(actionMessage.movement);
            } 
            catch (ConnectionError e) 
            {
                player.markAsDisconnected();
            }
        }
    }

    public Direction requestMovement()
    {
        return movementEvent.requestMovement();
    } 

    public Player getPlayer()
    {
        return player;
    }
}
