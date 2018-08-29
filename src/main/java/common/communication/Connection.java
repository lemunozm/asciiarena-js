package main.java.common.communication;

import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.net.Socket;

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
            System.out.println(object.toString());
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
            System.out.println(object.toString());

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
