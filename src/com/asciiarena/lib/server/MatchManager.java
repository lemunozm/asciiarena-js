package com.asciiarena.lib.server;

import com.asciiarena.lib.common.logging.Log;
import com.asciiarena.lib.server.player.PlayerRegistry;

public class MatchManager
{
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
        //TODO
        Log.info("Finish match");
    }
}
