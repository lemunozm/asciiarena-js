package main

import "os"
import "github.com/urfave/cli"
import "github.com/lemunozm/ASCIIArena/client"

func main() {
	commandApp := cli.NewApp()

	hostFlag := cli.StringFlag{
		Name:  "host",
		Usage: "Set the server `address`",
	}
	portFlag := cli.UintFlag{
		Name:  "port, p",
		Value: 3000,
		Usage: "Set the UDP port `number` for connecting to the server",
	}

	commandApp.CustomAppHelpTemplate = helpTemplate()
	commandApp.Name = "ASCIIArena-client"
	commandApp.Version = "0.0.0"
	commandApp.Usage = "Run the ASCIIArena client side"
	commandApp.Flags = []cli.Flag{hostFlag, portFlag}
	commandApp.Action = onLoad
	commandApp.Run(os.Args)
}

func helpTemplate() string {
	var name string = "NAME:\n    {{.Name}} - {{.Usage}}\n\n"
	var version string = "VERSION\n    {{.Version}}\n\n"
	var usage string = "USAGE:\n    {{.HelpName}} {{if .VisibleFlags}}[options]{{end}}\n    {{if len .Commands}}\n"
	var options string = "OPTIONS:\n    {{range .VisibleFlags}}{{.}}\n    {{end}}{{end}}{{if .Copyright }}\n"
	var endTemplate string = "{{end}}"
	return name + version + usage + options + endTemplate
}

func onLoad(context *cli.Context) error {
	if context.String("host") == "" {
		return cli.NewExitError("You must specify a host", 0)
	}

	clientApp := client.NewClient()
	clientApp.Run(context.String("host"), context.Uint("port"))

	return nil
}
