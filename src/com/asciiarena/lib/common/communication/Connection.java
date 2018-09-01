package com.asciiarena.lib.common.communication;

import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.net.Socket;

import com.asciiarena.lib.common.logging.Log;
import com.asciiarena.lib.common.logging.TermColor;

public class Connection
{
    private Socket socket;

    public Connection(Socket socket)
    {
        this.socket = socket; 
    }

    public boolean send(Object object)
    {
        try
        {
            ObjectOutputStream objectOutput = new ObjectOutputStream(socket.getOutputStream());
            objectOutput.writeObject(object); 

            String message = TermColor.YELLOW + "[" + object.toString() + "]" + TermColor.RESET;
            String remote = TermColor.PURPLE + socket.getRemoteSocketAddress().toString().substring(1) + TermColor.RESET;
            Log.info("%s to: %s", message, remote);  
        } 
        catch (IOException e)
        {
            e.printStackTrace();
        }
        return false;
    }

    public Object receive()
    {
        try
        {
            ObjectInputStream objectInput = new ObjectInputStream(socket.getInputStream());
            Object object = objectInput.readObject();

            String message = TermColor.BLUE + "[" + object.toString() + "]" + TermColor.RESET;
            String remote = TermColor.PURPLE + socket.getRemoteSocketAddress().toString().substring(1) + TermColor.RESET;
            Log.info("%s from: %s", message, remote);  

            return object;
        }
        catch (IOException e)
        {
            e.printStackTrace();
        }
        catch (ClassNotFoundException e)
        {
            e.printStackTrace();
        }

        return null;
    }

    public void close()
    {
        try
        {
            this.socket.close();
        } 
        catch (IOException e)
        {
            e.printStackTrace();
        }
    }
}
