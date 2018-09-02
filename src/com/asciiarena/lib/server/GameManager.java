package com.asciiarena.lib.server;

import com.asciiarena.lib.common.communication.Connection;
import com.asciiarena.lib.common.communication.Message;
import com.asciiarena.lib.common.logging.Log;
import com.asciiarena.lib.server.player.PlayerRegistry;

public class GameManager
{
    private PlayerRegistry playerRegistry;

    public GameManager(ServerConfig.GameConfig config)
    {
        this.playerRegistry = new PlayerRegistry(config.players, config.pointsToWin);
    }

    public boolean login(char character, Connection connection)
    {
        Message.PlayerLogin playerLoginMessage = new Message.PlayerLogin(); 
        playerLoginMessage.logged = registerPlayer(character, connection);
        connection.send(playerLoginMessage);

        if(playerLoginMessage.logged == true)
        {
            Message.PlayersInfo playersInfoMessage = new Message.PlayersInfo(playerRegistry.getCharacters()); 
            playerRegistry.sendToPlayers(playersInfoMessage);
        }

        return playerLoginMessage.logged;
    }

    public boolean registerPlayer(char character, Connection connection)
    {
        switch(playerRegistry.add(character, connection))
        {
            case OK:
                Log.info("Login player '%c'", character);
                return true;

            case ALREADY_EXISTS:
                Log.warning("Login player '%c': character already exists", character);
            default:
                return false;
        }
    }

    public void startGame()
    {
        Log.info("Start game");

        Log.info("Finish game");
    }

    public PlayerRegistry getPlayerRegistry()
    {
        return playerRegistry;
    }
}
