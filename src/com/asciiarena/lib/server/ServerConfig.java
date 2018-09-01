package com.asciiarena.lib.server;

public class ServerConfig
{
    public class InfoConfig
    {
        public int port;
    }

    public class GameConfig 
    {
        public class MapConfig 
        {
            public int width;
            public int height;
            public String seed;
        }

        public int port;
        public int players;
        public int pointsToWin;
        public MapConfig map = new MapConfig();
    }

    public InfoConfig info = new InfoConfig();
    public GameConfig game = new GameConfig();
}