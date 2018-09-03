package com.asciiarena.app.mode;

import java.util.logging.Level;

import org.apache.commons.cli.CommandLine;
import org.apache.commons.cli.CommandLineParser;
import org.apache.commons.cli.DefaultParser;
import org.apache.commons.cli.HelpFormatter;
import org.apache.commons.cli.Option;
import org.apache.commons.cli.Options;
import org.apache.commons.cli.ParseException;

import com.asciiarena.lib.common.logging.Log;
import com.asciiarena.lib.server.Server;
import com.asciiarena.lib.server.ServerConfig;

public class ServerMode
{
    private static final String HELP = "h";
    private static final String PORT = "port";
    private static final String PLAYERS = "p";
    private static final String POINTS = "points";
    private static final String WIDTH = "mw";
    private static final String HEIGHT = "mh";
    private static final String SEED = "s";
    private static final String LOG = "log";

    private ServerConfig config;
    private Level level;

    public ServerMode(String[] args)
    {
        this.config = new ServerConfig();
        this.config.port = 3000;
        this.config.game.players = 2;
        this.config.game.pointsToWin = config.game.players * 5;
        this.config.game.map.width = 30;
        this.config.game.map.height = 30;
        this.config.game.map.seed = "";
        this.level = Level.INFO;

        Options options = setupOptions();
        if(loadFromArgs(options, args)) 
        {
            Log.init(null);
            Log.level(level);

            Server server = new Server(config);
            server.listen();
        }
    }

    private Options setupOptions()
    {
        Options options = new Options();

        options.addOption(HELP, "help", false, "Show the help.");

        options.addOption(Option.builder(PORT)
                .desc("Server port. Default is: " + config.port + ".")
                .hasArg()
                .argName("number")
                .type(Number.class)
                .build());

        options.addOption(Option.builder(PLAYERS)
                .longOpt("players")
                .desc("Match player number.")
                .hasArg()
                .argName("number")
                .type(Number.class)
                .build());

        options.addOption(Option.builder(POINTS)
                .desc("Necesary points to win the game. The first players to reach this value win the game")
                .hasArg()
                .argName("number")
                .type(Number.class)
                .build());

        options.addOption(Option.builder(WIDTH)
                .longOpt("width")
                .desc("Map width")
                .hasArg()
                .argName("number")
                .type(Number.class)
                .build());

        options.addOption(Option.builder(HEIGHT)
                .longOpt("height")
                .desc("Map height")
                .hasArg()
                .argName("number")
                .type(Number.class)
                .build());

        options.addOption(Option.builder(SEED)
                .longOpt("seed")
                .desc("Map generation seed")
                .hasArg()
                .argName("string")
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

            if(cmd.hasOption(HELP))
            {
                formatter.printHelp("AsciiArena server", options, true); 
                return false;
            }

            if(cmd.hasOption(PORT))
            {
                config.port = ((Number)cmd.getParsedOptionValue(PORT)).intValue();
            }

            if(cmd.hasOption(PLAYERS))
            {
                config.game.players = ((Number)cmd.getParsedOptionValue(PLAYERS)).intValue();
            }

            if(cmd.hasOption(WIDTH))
            {
                config.game.map.width = ((Number)cmd.getParsedOptionValue(WIDTH)).intValue();
            }

            if(cmd.hasOption(HEIGHT))
            {
                config.game.map.height = ((Number)cmd.getParsedOptionValue(HEIGHT)).intValue();
            }

            if(cmd.hasOption(SEED))
            {
                config.game.map.seed = cmd.getOptionValue(HEIGHT);
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
            formatter.printHelp("AsciiArena server", options, true); 
            return false;
        }       

        return true;
    }
}
