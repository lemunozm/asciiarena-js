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

    public void send(Object object) throws ConnectionError
    {
        try
        {
            ObjectOutputStream objectOutput = new ObjectOutputStream(socket.getOutputStream());
            objectOutput.writeObject(object); 

            Log.info("%s to: %s", formatMessage(TermColor.YELLOW, object.toString()), formatAddress(socket));  
        } 
        catch (IOException e)
        {
            throw new ConnectionError(e, formatAddress(socket));
        }
    }

    public Object receive() throws ConnectionError
    {
        try
        {
            ObjectInputStream objectInput = new ObjectInputStream(socket.getInputStream());
            Object object = objectInput.readObject();

            Log.info("%s from: %s", formatMessage(TermColor.BLUE, object.toString()), formatAddress(socket));  

            return object;
        }
        catch (Exception e)
        {
            throw new ConnectionError(e, formatAddress(socket));
        }
    }

    public void close()
    {
        try
        {
            socket.close();
        } 
        catch (IOException e)
        {
            e.printStackTrace();
        }
    }

    private static String formatAddress(Socket socket)
    {
        return TermColor.PURPLE + socket.getRemoteSocketAddress().toString().substring(1) + TermColor.RESET;
    }

    private static String formatMessage(TermColor color, String message)
    {
        return color + "[" + message + "]" + TermColor.RESET;
    }
}
