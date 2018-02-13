package main

import "os"
import "github.com/urfave/cli"
import "github.com/lemunozm/ASCIIArena/common"
import "github.com/lemunozm/ASCIIArena/client"

func main() {
	commandApp := cli.NewApp()

	hostFlag := cli.StringFlag{
		Name:  "host",
		Usage: "Set the server address",
	}
	portFlag := cli.UintFlag{
		Name:  "port",
		Value: 3000,
		Usage: "Set the UDP port number for connecting to the server",
	}

	commandApp.CustomAppHelpTemplate = common.HelpCliTemplate()
	commandApp.Name = "ASCIIArena-client"
	commandApp.Version = common.GetVersion()
	commandApp.Usage = "Run the ASCIIArena client side"
	commandApp.Flags = []cli.Flag{hostFlag, portFlag}
	commandApp.Action = onLoad
	commandApp.Run(os.Args)
}

func onLoad(context *cli.Context) error {
	if context.String("host") == "" {
		return cli.NewExitError("You must specify a host", 0)
	}

	clientApp := client.NewClient(context.String("host"), context.Uint("port"))
	clientApp.Run()
	clientApp.Close()

	return nil
}
