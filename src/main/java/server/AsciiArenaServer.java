package main.java.server;

public class AsciiArenaServer
{
    public static void main(String[] args) 
    {
        ServerConfig config = new ServerConfig();
        config.info.port = 3000;
        config.game.port = 3001;
        config.game.players = 4;
        config.game.pointsToWin = 1;
        config.game.map.width = 30;
        config.game.map.height = 30;
        config.game.map.seed = "";

        Server server = new Server(config);
        server.run();

        System.out.println("Hello Ascii Arena");
    }
}
