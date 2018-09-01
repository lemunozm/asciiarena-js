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

        public int port; 
        public int currentPlayers; 
        public int maxPlayers; 

        public ServerInfo() {}
        public ServerInfo(int port, int currentPlayers, int maxPlayers)
        {
            this.port = port;
            this.currentPlayers = currentPlayers;
            this.maxPlayers = maxPlayers;
        }

        @Override
        public String toString()
        {
            return String.format("SERVER_INFO | %d | %d | %d", port, currentPlayers, maxPlayers);
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
        public static enum Status
        {
            SUCCESSFUL,
            ERROR_GAME_STARTED,
            ERROR_CHARACTER_EXISTS;
        }
            
        public Status status;
        public int maxPlayers;

        public PlayerLogin() {}
        public PlayerLogin(Status status, int maxPlayers)
        {
            this.status = status;
            this.maxPlayers = maxPlayers;
        }

        @Override
        public String toString()
        {
            return String.format("PLAYER_LOGIN | %s | %d", status, maxPlayers);
        }
    }

    public static class PlayersInfo implements Serializable
    {
        private static final long serialVersionUID = -3840805373060659823L;

        public List<Character> characters;

        public PlayersInfo() {}
        public PlayersInfo(List<Character> characters)
        {
            this.characters = characters;
        }

        @Override
        public String toString()
        {
            return String.format("PLAYER_INFO | %s", characters);
        }
    }

}
