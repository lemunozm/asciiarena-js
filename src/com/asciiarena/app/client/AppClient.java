package com.asciiarena.app.client;

import org.apache.commons.cli.Options;

import com.asciiarena.lib.client.Client;

public class AppClient
{
    public static void main(String[] args) 
    {
        Options options = new Options();
        options.addOption("t", false, "display current time");

        Client client = new Client("127.0.0.1", 3000);
        client.start();
    }
}
