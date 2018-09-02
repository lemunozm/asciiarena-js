package com.asciiarena.lib.common.communication;

import java.io.Serializable;
import java.util.List;

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

        public ServerInfo() {}
        public ServerInfo(List<Character> players, int maxPlayers)
        {
            this.players = players;
            this.maxPlayers = maxPlayers;
        }

        @Override
        public String toString()
        {
            return String.format("SERVER_INFO | %s | %d", players, maxPlayers);
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
        private static final long serialVersionUID = -7996103842250877133L;

        public boolean logged;

        public PlayerLogin() {}
        public PlayerLogin(boolean logged)
        {
            this.logged = logged;
        }

        @Override
        public String toString()
        {
            return String.format("PLAYER_LOGIN | %b", logged);
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
}
