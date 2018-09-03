package com.asciiarena.app.mode;

import org.apache.commons.cli.Options;

import com.asciiarena.lib.client.Client;
import com.asciiarena.lib.common.logging.Log;

public class ClientMode
{
    public static void start(String[] args) 
    {
        Options options = new Options();
        options.addOption("t", false, "display current time");

        Log.init("client.log");

        Client client = new Client("127.0.0.1", 3000);
        client.start();
    }
}
