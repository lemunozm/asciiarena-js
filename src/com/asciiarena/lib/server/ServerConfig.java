package com.asciiarena.lib.server;

public class ServerConfig
{
    public class GameConfig 
    {
        public class MapConfig 
        {
            public int width = 30;
            public int height = 30;
            public String seed = "";
        }

        public int players = 4;
        public int pointsToWin = 15;
        public MapConfig map = new MapConfig();
    }

    public int port = 3000;
    public GameConfig game = new GameConfig();
}