package com.asciiarena.lib.server;

import com.asciiarena.lib.common.communication.Connection;
import com.asciiarena.lib.common.communication.Message;
import com.asciiarena.lib.common.logging.Log;
import com.asciiarena.lib.server.player.PlayerRegistry;

public class GameManager
{
    private final ServerConfig.GameConfig config;
    private PlayerRegistry playerRegistry;
    private MatchManager currentMatch;

    public GameManager(ServerConfig.GameConfig config)
    {
        this.config = config;
        this.playerRegistry = new PlayerRegistry(config.players, config.pointsToWin);
        this.currentMatch = null;
    }

    public boolean login(Connection connection)
    {
        Message.NewPlayer newPlayerMessage = (Message.NewPlayer) connection.receive();
        Message.PlayerLogin playerLoginMessage = new Message.PlayerLogin(); 

        synchronized(this)
        {
            playerLoginMessage.logged = registerPlayer(newPlayerMessage.character, connection);
            connection.send(playerLoginMessage);

            if(playerLoginMessage.logged == true)
            {
                Message.PlayersInfo playersInfoMessage = new Message.PlayersInfo(playerRegistry.getCharacters()); 
                playerRegistry.sendToPlayers(playersInfoMessage);
            }
        }

        return playerLoginMessage.logged;
    }

    private boolean registerPlayer(char character, Connection connection)
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

        while(!playerRegistry.hasWinner())
        {
            currentMatch = new MatchManager(config.map, playerRegistry); 
            currentMatch.startMatch();
            break; //DELETE 
        }

        currentMatch = null;

        Log.info("Finish game");
    }

    public boolean isGameStarted()
    {
        return currentMatch != null;
    }

    public MatchManager getCurrentMatch()
    {
        return  currentMatch;
    }

    public PlayerRegistry getPlayerRegistry()
    {
        return playerRegistry;
    }
}
