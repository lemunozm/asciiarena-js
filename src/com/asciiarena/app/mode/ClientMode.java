package com.asciiarena.app.mode;

import java.util.logging.Level;

import org.apache.commons.cli.CommandLine;
import org.apache.commons.cli.CommandLineParser;
import org.apache.commons.cli.DefaultParser;
import org.apache.commons.cli.HelpFormatter;
import org.apache.commons.cli.Option;
import org.apache.commons.cli.Options;
import org.apache.commons.cli.ParseException;

import com.asciiarena.lib.client.Client;
import com.asciiarena.lib.common.logging.Log;

public class ClientMode
{
    private static final String HELP = "h";
    private static final String HOST = "host";
    private static final String PORT = "port";
    private static final String CHARACTER = "c";
    private static final String LOG = "log";

    private String host;
    private int port;
    private char character; 
    private Level level;

    public ClientMode(String[] args)
    {
        this.port = 3000;
        this.character = Client.ASK_FOR_CHARACTER;
        this.level = Level.INFO;

        Options options = setupOptions();
        if(loadFromArgs(options, args)) 
        {
            Log.init("client.log");
            Log.level(level);

            Client client = new Client(host, port, character);
            client.start();
        }
    }

    private Options setupOptions()
    {
        Options options = new Options();

        options.addOption(HELP, "help", false, "Show the help.");

        options.addOption(Option.builder(HOST)
                .desc("Server host. It can be the domain or the ip.")
                .hasArg()
                .argName("domain/ip")
                .required()
                .build());

        options.addOption(Option.builder(PORT)
                .desc("Server port. Default is: " + port + ".")
                .hasArg()
                .argName("number")
                .type(Number.class)
                .build());

        options.addOption(Option.builder(CHARACTER)
                .longOpt("character")
                .desc("Default player character. It must be a capital letter. "
                    + "If it not set or the character is already used, "
                    + "the application will ask the character to the user.")
                .hasArg()
                .argName("character")
                .type(Character.class)
                .build());

        options.addOption(Option.builder(LOG)
                .desc("Set the log level:\n"
                    + "level=off: disable the logger\n"
                    + "level=error: show only critical errors messages\n"
                    + "level=warning: show errors and warnings messages\n"
                    + "level=info: show all log messages\n"
                    + "by default is info.")
                .hasArg()
                .argName("level")
                .build());

        return options;
    }

    private boolean loadFromArgs(Options options, String[] args) 
    {
        HelpFormatter formatter = new HelpFormatter();
        formatter.setWidth(90);

        try
        {
            CommandLineParser parser = new DefaultParser();
            CommandLine cmd = parser.parse(options, args);

            host = cmd.getOptionValue(HOST);

            if(cmd.hasOption(HELP))
            {
                formatter.printHelp("AsciiArena client", options, true); 
                return false;
            }

            if(cmd.hasOption(PORT))
            {
                port = ((Number)cmd.getParsedOptionValue(PORT)).intValue();
            }

            if(cmd.hasOption(CHARACTER))
            {
                char inputCharacter = cmd.getOptionValue(CHARACTER).charAt(0);
                if(Character.isUpperCase(inputCharacter) && cmd.getOptionValue(CHARACTER).length() == 1)
                {
                    character = inputCharacter;
                }
                else
                {
                    System.out.println("The character must be a capital letter");
                    return false;
                }
            }

            if(cmd.hasOption(LOG))
            {
                switch(cmd.getOptionValue(LOG))
                {
                    case "off":
                        level = Level.OFF;
                        break;
                    case "error":
                        level = Level.SEVERE;
                        break;
                    case "warning":
                        level = Level.WARNING;
                        break;
                    case "info":
                        level = Level.INFO;
                        break;
                    default:
                        System.out.println("The log level must be a valid value");
                        return false;
                }
            }
        } 
        catch (ParseException e)
        {
            System.out.println(e.getMessage());
            formatter.printHelp("AsciiArena client", options, true); 
            return false;
        }       

        return true;
    }
}
