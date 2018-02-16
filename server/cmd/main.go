package main

import "os"
import "github.com/urfave/cli"
import "github.com/lemunozm/ASCIIArena/common"
import "github.com/lemunozm/ASCIIArena/server"

func main() {
	commandApp := cli.NewApp()

	portFlag := cli.UintFlag{
		Name:  "local-tcp-port, tp",
		Usage: "Set the UDP port number for connecting to the server",
		Value: 3000,
	}

	playersFlag := cli.UintFlag{
		Name:  "players, p",
		Usage: "Set the number of players for the match",
	}

	waitMatchFlag := cli.UintFlag{
		Name:  "wait-match",
		Usage: "Waiting in milliseconds to initialize the match once all players are connected",
		Value: 3000,
	}

	mapSeedFlag := cli.UintFlag{
		Name:  "map-seed, s",
		Usage: "Seed for generate a map. 0 means that the maps will be generated randomly",
		Value: 0,
	}

	commandApp.CustomAppHelpTemplate = common.HelpCliTemplate()
	commandApp.Name = "ASCIIArena-server"
	commandApp.Version = common.GetVersion()
	commandApp.Usage = "Run the ASCIIArena server side"
	commandApp.Flags = []cli.Flag{portFlag, playersFlag, waitMatchFlag, mapSeedFlag}
	commandApp.Action = onLoad
	commandApp.Run(os.Args)
}

func onLoad(c *cli.Context) error {
	if c.Uint("players") == 0 {
		return cli.NewExitError("You must specify a player number", 0)
	}

	serverApp := server.NewServer(c.Uint("local-tcp-port"), c.Uint("players"))
	serverApp.Run()

	return nil
}
