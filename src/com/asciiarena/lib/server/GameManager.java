package com.asciiarena.lib.server;

import com.asciiarena.lib.common.communication.Connection;
import com.asciiarena.lib.common.communication.Message;
import com.asciiarena.lib.common.logging.Log;
import com.asciiarena.lib.server.player.PlayerRegistry;

public class GameManager
{
    private PlayerRegistry playerRegistry;
    private boolean gameStarted;

    public GameManager(ServerConfig.GameConfig config)
    {
        this.playerRegistry = new PlayerRegistry(config.players, config.pointsToWin);
        this.gameStarted = false;
    }

    public boolean registerPlayer(Connection connection)
    {
        Message.NewPlayer newPlayerMessage = (Message.NewPlayer) connection.receive();
        Message.PlayerLogin.Status loginStatus = Message.PlayerLogin.Status.ERROR_GAME_STARTED;
        if(!gameStarted)
        {
            switch(playerRegistry.add(newPlayerMessage.character, connection))
            {
                case OK:
                    Log.info("Login player '%c'", newPlayerMessage.character);
                    loginStatus = Message.PlayerLogin.Status.SUCCESSFUL;
                    break;

                case FULL:
                    Log.warning("Login player '%c': full players", newPlayerMessage.character);
                    loginStatus = Message.PlayerLogin.Status.ERROR_GAME_STARTED;
                    break;

                case ALREADY_EXISTS:
                    Log.warning("Login player '%c': characters exists", newPlayerMessage.character);
                    loginStatus = Message.PlayerLogin.Status.ERROR_CHARACTER_EXISTS;
                    break;
            }
        }

        Message.PlayerLogin playerLoginMessage = new Message.PlayerLogin(); 
        playerLoginMessage.status = loginStatus;
        playerLoginMessage.maxPlayers = playerRegistry.getMaxPlayers();
        connection.send(playerLoginMessage);

        if(loginStatus == Message.PlayerLogin.Status.SUCCESSFUL)
        {
            Message.PlayersInfo playersInfoMessage = new Message.PlayersInfo(playerRegistry.getCharacters()); 
            playerRegistry.sendToPlayers(playersInfoMessage);
            return true;
        }

        return false;
    }

    public void startGame()
    {
        gameStarted = true;
        Log.info("Start game");
        //TODO
        Log.info("Finish game");
        gameStarted = false;
    }

    public boolean isGameStarted()
    {
        return gameStarted;
    }

    public boolean isReadyToStartGame()
    {
        return playerRegistry.getCurrentPlayers() == playerRegistry.getMaxPlayers() && !gameStarted; 
    }

    public PlayerRegistry getPlayerRegistry()
    {
        return playerRegistry;
    }
}
