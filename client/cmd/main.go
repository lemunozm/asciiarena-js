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
	remoteTCPPortFlag := cli.UintFlag{
		Name:  "remote-tcp-port, tp",
		Value: 3000,
		Usage: "Set the TCP port number for connecting to the server",
	}
	localUDPPortFlag := cli.UintFlag{
		Name:  "local-udp-port, lp",
		Value: 3000,
		Usage: "Set the UDP port number for connecting to the server",
	}

	commandApp.CustomAppHelpTemplate = common.HelpCliTemplate()
	commandApp.Name = "ASCIIArena-client"
	commandApp.Version = common.GetVersion()
	commandApp.Usage = "Run the ASCIIArena client side"
	commandApp.Flags = []cli.Flag{hostFlag, remoteTCPPortFlag, localUDPPortFlag}
	commandApp.Action = onLoad
	commandApp.Run(os.Args)
}

func onLoad(c *cli.Context) error {
	if c.String("host") == "" {
		return cli.NewExitError("You must specify a host", 0)
	}

	clientApp := client.NewClient(c.String("host"), c.Uint("remote-tcp-port"), c.Uint("local-udp_port"))
	clientApp.Run()

	return nil
}
