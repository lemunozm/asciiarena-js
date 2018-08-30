package com.asciiarena.client;

import java.io.IOException;
import java.net.Socket;

import com.asciiarena.common.communication.Connection;
import com.asciiarena.common.communication.Message;
import com.asciiarena.common.logging.Log;

public class AsciiArenaClient
{
    public static void main(String[] args) 
    {
        Log.init();
        try
        {
            Socket socket = new Socket("127.0.0.1", 3000);
            Connection connection = new Connection(socket);

            Message.Version versionMessage = new Message.Version("1.0.0");
            connection.send(versionMessage);

            Message.CheckedVersion checkedVersionMessage = (Message.CheckedVersion) connection.receive();
            System.out.println(checkedVersionMessage.validation);
        } 
        catch (IOException e)
        {
            e.printStackTrace();
        }    
    }
}
