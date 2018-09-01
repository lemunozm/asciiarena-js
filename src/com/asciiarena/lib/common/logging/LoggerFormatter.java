package com.asciiarena.lib.common.logging;

import java.util.Date;
import java.util.logging.Level;
import java.util.logging.LogRecord;
import java.util.logging.SimpleFormatter;

public class LoggerFormatter extends SimpleFormatter
{
    

    @Override
    public String format(LogRecord record)
    {
        String dateFormat = TermColor.GREY_LIGHT + "%1$tF %1$tT" + TermColor.RESET;
        String levelFormat = getLevelColor(record.getLevel()) + "%2$-7s" + TermColor.RESET;
        String logFormat = dateFormat + " " + levelFormat + " %3$s%n" + TermColor.RESET;

        Date date = new Date(record.getMillis()); 
        String level = record.getLevel().toString();

        return String.format(logFormat, date, level, record.getMessage());
    }

    private static TermColor getLevelColor(Level level)
    {
        if(level == Level.INFO)
        {
            return TermColor.CYAN;
        }
        else if(level == Level.WARNING)
        {
            return TermColor.YELLOW_DARK;
        }
        else if(level == Level.SEVERE)
        {
            return TermColor.RED;
        }
        else
        {
            return TermColor.WHITE; 
        }
    }
}
