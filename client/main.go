package main

import "fmt"
import "os"
import "github.com/urfave/cli"

func main() {
	app := cli.NewApp()

	host := cli.StringFlag{
		Name:  "host",
		Usage: "Set the server `address`",
	}
	port := cli.UintFlag{
		Name:  "port, p",
		Value: 3000,
		Usage: "Set the UDP port `number` for connecting to the server",
	}

	app.Name = "ASCIIArena-client"
	app.Version = "0.0.0"
	app.Usage = "Run the ASCIIArena client side"
	app.Flags = []cli.Flag{host, port}
	app.Action = load
	app.Run(os.Args)
}

func load(context *cli.Context) error {

	//check
	//clientApp := client.NewClient()
	//clientApp.Run()

	return nil
}
