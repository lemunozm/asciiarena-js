package com.asciiarena.lib.common.logging;

import java.io.IOException;
import java.util.logging.ConsoleHandler;
import java.util.logging.FileHandler;
import java.util.logging.Handler;
import java.util.logging.Level;

public final class Log
{
    private static java.util.logging.Logger log = null;

    public static void init(String fileName)
    {
        Handler handler;
        if(fileName == null)
        {
            handler = new ConsoleHandler();
        }
        else
        {
            try
            {
                handler = new FileHandler(fileName);
            } 
            catch (SecurityException e)
            {
                e.printStackTrace();
                return;
            } 
            catch (IOException e)
            {
                e.printStackTrace();
                return;
            }   
        }

        handler.setFormatter(new LoggerFormatter());

        log = java.util.logging.Logger.getLogger("com.asciiarena");
        log.addHandler(handler);
        log.setUseParentHandlers(false);
        log.setLevel(Level.INFO);
    }

    public static void info(String format, Object... args)
    {
        if(log != null && log.isLoggable(Level.INFO))
        {
            log.info(String.format(format, args)); 
        }
    }

    public static void warning(String format, Object... args)
    {
        if(log != null && log.isLoggable(Level.WARNING))
        {
            log.warning(String.format(format, args)); 
        }
    }

    public static void error(String format, Object... args)
    {
        if(log != null && log.isLoggable(Level.SEVERE))
        {
            log.severe(String.format(format, args)); 
        }
    }

    public static void level(Level level)
    {
        if(log != null)
        {
            log.setLevel(level);
        }
    }
}
