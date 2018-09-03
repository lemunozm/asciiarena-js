package com.asciiarena.lib.server;

public class ServerConfig
{
    public class GameConfig 
    {
        public class MapConfig 
        {
            public int width;
            public int height;
            public String seed;
        }

        public int players;
        public int pointsToWin;
        public MapConfig map = new MapConfig();
    }

    public int port;
    public GameConfig game = new GameConfig();
}