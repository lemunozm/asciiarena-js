package main.java.client;

import java.io.IOException;
import java.net.Socket;

import main.java.common.communication.Connection;
import main.java.common.communication.Message;

public class AsciiArenaClient
{
    public static void main(String[] args) 
    {
        System.out.println("Hello AsciiArena");
        try
        {
            Socket socket = new Socket("127.0.0.1", 3000);
            Connection connection = new Connection(socket);

            Message.Version versionMessage = new Message.Version();
            versionMessage.version = "1.0.0";
            connection.send(versionMessage);
        } 
        catch (IOException e)
        {
            e.printStackTrace();
        }    
    }
}
