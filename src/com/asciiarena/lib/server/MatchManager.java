package com.asciiarena.lib.server;

import java.util.ArrayList;
import java.util.Random;

import com.asciiarena.lib.common.communication.Message;
import com.asciiarena.lib.common.match.Entity;
import com.asciiarena.lib.common.match.MatchSynchronization;
import com.asciiarena.lib.server.match.EntityAction;
import com.asciiarena.lib.server.match.Match;
import com.asciiarena.lib.server.player.Player;
import com.asciiarena.lib.server.player.PlayerRegistry;

public class MatchManager
{
    private static final int RANDOM_SEED_LENGTH = 20;

    private PlayerRegistry playerRegistry;
    private ArrayList<PlayerEventManager> playerEventManagers;
    private String seed;
    private Match match;
    private MatchSynchronization matchSynchronization;

    public MatchManager(ServerConfig.GameConfig.MapConfig mapConfig, PlayerRegistry registry)
    {
        this.playerRegistry = registry;
        this.playerEventManagers = new ArrayList<PlayerEventManager>();
        this.seed = mapConfig.seed.equals("") ? generateRandomSeed() : mapConfig.seed;
        this.match = new Match(mapConfig.width, mapConfig.height, seed, playerRegistry.getCharacters());
        this.matchSynchronization = new MatchSynchronization();
    }

    public void init()
    {
        Message.MatchInfo matchInfoMessage = new Message.MatchInfo();
        matchInfoMessage.seed = seed;
        matchInfoMessage.grid = match.getMap().getGrid();
        matchInfoMessage.entities = match.getEntities();
        playerRegistry.sendToPlayers(matchInfoMessage);

        for(Player player: playerRegistry.getPlayers())
        {
            playerEventManagers.add(new PlayerEventManager(player));
        }
    }

    public void update()
    {
        matchSynchronization.waitForNextFrame();

        ArrayList<EntityAction> entityActions = new ArrayList<EntityAction>(); 

        for(PlayerEventManager playerEvent: playerEventManagers)
        {
            Player player = playerEvent.getPlayer();
            if(player.isConnected())
            {
                Entity entity = match.getEntity(player.getCharacter());
                entityActions.add(new EntityAction(entity, playerEvent.requestMovement())); 
            }
        }

        match.update(entityActions);
        entityActions.clear();

        Message.Frame frameMessage = new Message.Frame();
        frameMessage.entities = match.getEntities();
        playerRegistry.sendToPlayers(frameMessage);
    }

    public boolean hasFinished()
    {
        return match.hasFinished();
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