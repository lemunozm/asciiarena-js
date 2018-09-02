package com.asciiarena.app.client;

import com.asciiarena.lib.client.Client;

public class AppClient
{
    public static void main(String[] args) 
    {
        Client client = new Client("127.0.0.1", 3000);
        client.start();
    }
}
