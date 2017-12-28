package main

import cm "../common"
import "fmt"
import "os"

func main() {
	argumentList := cm.NewArgumentList()

	argumentList.Add(&cm.Argument{
		Name:        "help",
		Description: "Show help",
		Ids:         []string{"--help", "-h"},
		DisableRequiredArguments: true,
	})

	argumentList.Add(&cm.Argument{
		Name:          "port",
		Description:   "Set the port of the server",
		Ids:           []string{"--port"},
		ValuesName:    []string{"number"},
		DefaultValues: []string{"3000"},
	})

	argumentList.Add(&cm.Argument{
		Name:        "players",
		Description: "Set the number of players for the match",
		Ids:         []string{"--players", "-p"},
		ValuesName:  []string{"number"},
		Required:    true,
	})

	argumentList.Add(&cm.Argument{
		Name:          "waitMatch",
		Description:   "Waiting to initialize the match once all players are connected",
		Ids:           []string{"--wait-match"},
		ValuesName:    []string{"number"},
		DefaultValues: []string{"3000"},
	})

	argumentList.Add(&cm.Argument{
		Name:          "mapSeed",
		Description:   "Seed for generate a map. 0 means that the maps will be generated randomly",
		Ids:           []string{"--map-seed", "-ms"},
		ValuesName:    []string{"number"},
		DefaultValues: []string{"0"},
	})

	argumentList.Parse(os.Args)

	fmt.Println(argumentList)
}
