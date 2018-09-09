package com.asciiarena.lib.server;

import java.util.ArrayList;
import java.util.List;
import java.util.Random;

import com.asciiarena.lib.common.communication.Message;
import com.asciiarena.lib.common.match.Entity;
import com.asciiarena.lib.server.match.EntityAction;
import com.asciiarena.lib.server.match.Match;
import com.asciiarena.lib.server.player.Player;
import com.asciiarena.lib.server.player.PlayerRegistry;

import javafx.util.Pair;

public class MatchManager
{
    private static final int RANDOM_SEED_LENGTH = 20;

    private PlayerRegistry playerRegistry;
    private String seed;
    private Match match;
    private ArrayList<EntityAction> entityActions;

    public MatchManager(ServerConfig.GameConfig.MapConfig mapConfig, PlayerRegistry registry)
    {
        this.playerRegistry = registry;
        this.seed = mapConfig.seed.equals("") ? generateRandomSeed() : mapConfig.seed;
        this.match = new Match(mapConfig.width, mapConfig.height, seed, playerRegistry.getCharacters());
        this.entityActions = new ArrayList<EntityAction>(); 
    }

    public void init()
    {
        Message.MatchInfo matchInfoMessage = new Message.MatchInfo();
        matchInfoMessage.seed = seed;
        matchInfoMessage.grid = match.getMap().getGrid();
        matchInfoMessage.entities = match.getEntities();
        playerRegistry.sendToPlayers(matchInfoMessage);
    }

    public void update()
    {
        match.update(entityActions);
        entityActions.clear();

        Message.Frame frameMessage = new Message.Frame();
        frameMessage.entities = match.getEntities();
        playerRegistry.sendToPlayers(frameMessage);

        try
        {
            Thread.sleep(0);
        } 
        catch (InterruptedException e)
        {
            e.printStackTrace();
        }
    }

    public void playerActions()
    {
        List<Pair<Player, Object>> playerActionMessages = playerRegistry.receiveFromPlayers();

        for(Pair<Player, Object> message: playerActionMessages)
        {
            Player player = message.getKey();
            if(player.isConnected())
            {
                Message.PlayerAction action = (Message.PlayerAction) message.getValue();

                Entity entity = match.getEntity(player.getCharacter());
                entityActions.add(new EntityAction(entity, action.movement));
            }
        }
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