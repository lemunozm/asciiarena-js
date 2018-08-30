package com.asciiarena.common.logging;

import java.util.logging.ConsoleHandler;
import java.util.logging.Level;

public final class Log
{
    private static java.util.logging.Logger log = null;

    public static void init()
    {
        log = java.util.logging.Logger.getLogger("com.asciiarena");
        log.setUseParentHandlers(false);

        ConsoleHandler handler = new ConsoleHandler();
        handler.setFormatter(new LoggerFormatter());
        log.addHandler(handler);

        log.setLevel(Level.INFO);
    }

    public static void info(String format, Object... args)
    {
        if(log.isLoggable(Level.INFO))
        {
            log.info(String.format(format, args)); 
        }
    }

    public static void warning(String format, Object... args)
    {
        if(log.isLoggable(Level.WARNING))
        {
            log.warning(String.format(format, args)); 
        }
    }

    public static void error(String format, Object... args)
    {
        if(log.isLoggable(Level.SEVERE))
        {
            log.severe(String.format(format, args)); 
        }
    }
}
