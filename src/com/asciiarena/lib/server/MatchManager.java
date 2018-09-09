package com.asciiarena.lib.server;

import java.util.Random;

import com.asciiarena.lib.common.communication.Message;
import com.asciiarena.lib.common.logging.Log;
import com.asciiarena.lib.server.match.Match;
import com.asciiarena.lib.server.player.PlayerRegistry;

public class MatchManager
{
    private static final int RANDOM_SEED_LENGTH = 20;

    private final ServerConfig.GameConfig.MapConfig mapConfig;
    private PlayerRegistry playerRegistry;

    public MatchManager(ServerConfig.GameConfig.MapConfig mapConfig, PlayerRegistry registry)
    {
        this.mapConfig = mapConfig;
        this.playerRegistry = registry;
    }

    public void startMatch()
    {
        Log.info("Start match");

        String seed = mapConfig.seed.equals("") ? generateRandomSeed() : mapConfig.seed;
        Match match = new Match(mapConfig.width, mapConfig.height, seed, playerRegistry.getCharacters());

        Message.MatchInfo matchInfoMessage = new Message.MatchInfo();
        matchInfoMessage.seed = seed;
        matchInfoMessage.grid = match.getMap().getGrid();
        matchInfoMessage.entities = match.getEntities();

        playerRegistry.sendToPlayers(matchInfoMessage);

        //wait the time here

        Log.info("Finish match");
    }

    public static String generateRandomSeed()
    {
        String symbols = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890";
        Random random = new Random();
        StringBuilder seed = new StringBuilder(RANDOM_SEED_LENGTH);

        for(int i = 0; i < RANDOM_SEED_LENGTH; i++) 
        {
            seed.append(symbols.charAt(random.nextInt(symbols.length())));
        }

        return seed.toString();
    }
}