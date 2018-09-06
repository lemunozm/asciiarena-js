package com.asciiarena.lib.common.communication;

import java.io.Serializable;
import java.util.List;

import com.asciiarena.lib.common.match.Entity;
import com.asciiarena.lib.common.match.Wall;

public class Message 
{
    public static class Version implements Serializable
    {
        private static final long serialVersionUID = 6487528050142605112L;

        public String version; 

        public Version() {}
        public Version(String version)
        {
            this.version = version;
        }

        @Override
        public String toString()
        {
            return String.format("VERSION | %s", version);
        }
    }

    public static class CheckedVersion implements Serializable
    {
        private static final long serialVersionUID = -4190722298194654981L;

        public String version; 
        public boolean validation; 

        public CheckedVersion() {}
        public CheckedVersion(String version, boolean validation)
        {
            this.version = version;
            this.validation = validation;
        }

        @Override
        public String toString()
        {
            return String.format("CHECKED_VERSION | %s | %b", version, validation);
        }
    }

    public static class ServerInfo implements Serializable
    {
        private static final long serialVersionUID = -8246089342165465473L;

        public List<Character> players; 
        public int maxPlayers; 
        public int pointsToWin;

        public ServerInfo() {}
        public ServerInfo(List<Character> players, int maxPlayers, int pointsToWin)
        {
            this.players = players;
            this.maxPlayers = maxPlayers;
            this.pointsToWin = pointsToWin;
        }

        @Override
        public String toString()
        {
            return String.format("SERVER_INFO | %s | %d | %d", players, maxPlayers, pointsToWin);
        }
    }

    public static class NewPlayer implements Serializable
    {
        private static final long serialVersionUID = -7996103842250877133L;

        public char character; 

        public NewPlayer() {}
        public NewPlayer(char character)
        {
            this.character = character;
        }

        @Override
        public String toString()
        {
            return String.format("NEW_PLAYER | %c", character);
        }
    }

    public static class PlayerLogin implements Serializable
    {
        private static final long serialVersionUID = -8777686551827290213L;

        public static enum Status
        {
            SUCCESSFUL,
            CHARACTER_ALREADY_EXISTS,
            GAME_COMPLETE
        }

        public Status status;

        public PlayerLogin() {}
        public PlayerLogin(Status status)
        {
            this.status = status;
        }

        @Override
        public String toString()
        {
            return String.format("PLAYER_LOGIN | %s", status);
        }
    }

    public static class PlayersInfo implements Serializable
    {
        private static final long serialVersionUID = -3840805373060659823L;

        public List<Character> players;

        public PlayersInfo() {}
        public PlayersInfo(List<Character> players)
        {
            this.players = players;
        }

        @Override
        public String toString()
        {
            return String.format("PLAYER_INFO | %s", players);
        }
    }

    public static class MatchInfo implements Serializable
    {
        private static final long serialVersionUID = -366787905875060737L;

        public int width;
        public int height;
        public Wall grid[][]; 
        public String seed;
        public List<Entity> entities; 
        
        public MatchInfo() {}
        public MatchInfo(int width, int height, Wall grid[][], String seed, List<Entity> entities)
        {
            this.width = width;
            this.height = height;
            this.grid = grid;
            this.seed = seed;
            this.entities = entities;
        }

        @Override
        public String toString()
        {
            return String.format("MATCH_INFO | %d | %d | %s", width , height, seed);
        }
    }
}
