package main.java.server;

public class Server
{
    private ServerConfig config;

    public Server(ServerConfig config)
    {
        this.config = config;
    }

    public void run()
    {
        GameServer gameServer = new GameServer(this.config.game);

        Runnable gameServerRun = new Runnable() 
        {
            public void run() {
                gameServer.run();
            }
        };  

        Thread gameServerThread = new Thread(gameServerRun);
        gameServerThread.start();

        InfoServer infoServer = new InfoServer(this.config.info, gameServer);
        infoServer.run();
    }
}
