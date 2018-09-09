package com.asciiarena.lib.server;

import com.asciiarena.lib.common.communication.Connection;
import com.asciiarena.lib.common.communication.ConnectionError;
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

    public boolean checkGameInfo(Connection connection) throws ConnectionError
    {
        Message.GameInfo gameInfoMessage = new Message.GameInfo();
        gameInfoMessage.players = playerRegistry.getCharacters();
        gameInfoMessage.maxPlayers = playerRegistry.getMaxPlayers();
        gameInfoMessage.pointsToWin = playerRegistry.getPointsToWin();
        gameInfoMessage.mapWidth = config.map.width; 
        gameInfoMessage.mapHeight = config.map.height; 
        gameInfoMessage.defaultMapSeed = config.map.seed; 
        connection.send(gameInfoMessage);

        return !playerRegistry.isComplete();
    }

    public boolean login(Connection connection) throws ConnectionError
    {
        Message.NewPlayer newPlayerMessage = (Message.NewPlayer) connection.receive();
        Message.PlayerLogin playerLoginMessage = new Message.PlayerLogin(); 

        synchronized(this)
        {
            playerLoginMessage.status = registerPlayer(newPlayerMessage.character, connection);
            connection.send(playerLoginMessage);

            if(playerLoginMessage.status == Message.PlayerLogin.Status.SUCCESSFUL)
            {
                Message.PlayersInfo playersInfoMessage = new Message.PlayersInfo(playerRegistry.getCharacters()); 
                playerRegistry.sendToPlayers(playersInfoMessage);
            }
        }

        return playerLoginMessage.status == Message.PlayerLogin.Status.SUCCESSFUL;
    }

    private Message.PlayerLogin.Status registerPlayer(char character, Connection connection)
    {
        switch(playerRegistry.add(character, connection))
        {
            case OK:
                Log.info("Login player '%c': successful", character);
                return Message.PlayerLogin.Status.SUCCESSFUL;

            case ALREADY_EXISTS:
                Log.warning("Login player '%c': character already exists", character);
                return Message.PlayerLogin.Status.CHARACTER_ALREADY_EXISTS;

            case FULL:
                Log.warning("Login player '%c': game complete", character);
                return Message.PlayerLogin.Status.GAME_COMPLETE;

            default:
                return Message.PlayerLogin.Status.GAME_COMPLETE;
        }
    }

    public void startGame()
    {
        Log.info("Start game");

        while(!playerRegistry.hasWinner())
        {
            currentMatch = new MatchManager(config.map, playerRegistry); 
            currentMatch.startMatch();
            try
            {
                Thread.sleep(3600000);
            }
            catch (InterruptedException e)
            {
                e.printStackTrace();
            }
            System.exit(1);
        }

        currentMatch = null;

        Log.info("Finish game");
    }

    public void reset()
    {
        playerRegistry = new PlayerRegistry(config.players, config.pointsToWin);
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
