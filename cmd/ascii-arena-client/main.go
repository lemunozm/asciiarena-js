package main

import "github.com/lemunozm/ascii-arena/internal/client"
import "github.com/lemunozm/ascii-arena/internal/pkg/version"

import "gopkg.in/urfave/cli.v1"
import "os"

import "fmt"

func main() {
	commandApp := cli.NewApp()

	hostFlag := cli.StringFlag{
		Name:  "host, ip",
		Usage: "Server address ip",
	}

	TCPPortFlag := cli.IntFlag{
		Name:  "port, p",
		Value: 3001,
		Usage: "Server port",
	}

	characterFlag := cli.StringFlag{
		Name:  "character, c",
		Usage: "Select the character to play",
	}

	commandApp.CustomAppHelpTemplate = HelpCliTemplate()
	commandApp.Name = "ASCIIArena-client"
	commandApp.Version = version.Current
	commandApp.Usage = "Run the ASCIIArena client side"
	commandApp.Flags = []cli.Flag{hostFlag, TCPPortFlag, characterFlag}
	commandApp.Action = func(context *cli.Context) error {
		if context.String("host") == "" {
			return cli.NewExitError("You must to specify the server host", 1)
		}
		if context.String("character") == "" {
			return cli.NewExitError("You must to specify a character", 1)
		}

		fmt.Printf("%c\n", context.String("character")[0])
		c := client.NewClient(context.String("host"), context.Int("port"), context.String("character")[0])
		c.Run()
		return nil
	}
	commandApp.Run(os.Args)
}

func HelpCliTemplate() string {
	var name string = "NAME:\n    {{.Name}} - {{.Usage}}\n\n"
	var version string = "VERSION\n    {{.Version}}\n\n"
	var usage string = "USAGE:\n    {{.HelpName}} {{if .VisibleFlags}}[options]{{end}}\n    {{if len .Commands}}\n"
	var options string = "OPTIONS:\n    {{range .VisibleFlags}}{{.}}\n    {{end}}{{end}}{{if .Copyright }}\n"
	var endTemplate string = "{{end}}"
	return name + version + usage + options + endTemplate
}
