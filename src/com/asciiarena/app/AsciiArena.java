package com.asciiarena.app;

import java.util.Arrays;

import com.asciiarena.app.mode.ClientMode;
import com.asciiarena.app.mode.ServerMode;

public class AsciiArena
{
    public static void main(String[] args) 
    {
        if(args.length > 0)
        {
            String[] subArgs = Arrays.copyOfRange(args, 1, args.length);
            if(args[0].equals("client"))
            {
                ClientMode.start(subArgs); 
                return;
            }
            else if(args[0].equals("server"))
            {
                ServerMode.start(subArgs);
                return;
            }
        }

        System.out.println("Usage: AsciiArena [client | server]");
    }
}
