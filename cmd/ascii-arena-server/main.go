package main

import "github.com/lemunozm/ascii-arena/internal/server"
import "github.com/lemunozm/ascii-arena/internal/pkg/version"

import "gopkg.in/urfave/cli.v1"
import "os"

func main() {
	s := server.Server{
		GameTCPPort: 3000,
		InfoTCPPort: 3001,
		Players:     4,
		PointsToWin: 1,
		Map: server.MapConfig{
			Width:  30,
			Height: 30,
			Seed:   "",
		},
	}

	commandApp := cli.NewApp()

	gameTCPPortFlag := cli.IntFlag{
		Name:        "game-port",
		Value:       s.GameTCPPort,
		Usage:       "Game server port",
		Destination: &s.GameTCPPort,
	}

	infoTCPPortFlag := cli.IntFlag{
		Name:        "info-port",
		Value:       s.InfoTCPPort,
		Usage:       "Info server port",
		Destination: &s.InfoTCPPort,
	}

	playersFlag := cli.IntFlag{
		Name:        "players, p",
		Value:       s.Players,
		Usage:       "Necessary players for the match",
		Destination: &s.Players,
	}

	pointsToWinFlag := cli.IntFlag{
		Name:        "points",
		Value:       s.PointsToWin,
		Usage:       "Points to win the game",
		Destination: &s.PointsToWin,
	}

	mapWidthFlag := cli.IntFlag{
		Name:        "map-width",
		Value:       s.Map.Width,
		Usage:       "Width of the map",
		Destination: &s.Map.Width,
	}

	mapHeightFlag := cli.IntFlag{
		Name:        "map-height",
		Value:       s.Map.Height,
		Usage:       "Height of the map",
		Destination: &s.Map.Height,
	}

	mapSeedFlag := cli.StringFlag{
		Name:        "map-seed, s",
		Value:       s.Map.Seed,
		Usage:       "Seed used to generate the map (default: random seed is used)",
		Destination: &s.Map.Seed,
	}

	commandApp.CustomAppHelpTemplate = HelpCliTemplate()
	commandApp.Name = "ASCIIArena-server"
	commandApp.Version = version.Current
	commandApp.Usage = "Run the ASCIIArena server side"
	commandApp.Flags = []cli.Flag{gameTCPPortFlag, infoTCPPortFlag, playersFlag, pointsToWinFlag, mapWidthFlag, mapHeightFlag, mapSeedFlag}
	commandApp.Action = func(c *cli.Context) error {
		s.Run()
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
