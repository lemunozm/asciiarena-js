package main

import "github.com/lemunozm/ascii-arena/internal/server"

func main() {
	s := server.Server{
		TCPPortGame:       3000,
		TCPPortInfo:       3001,
		MaxPlayers:        4,
		PointsToWin:       1,
		InfoServerEnabled: true,
		Map: server.MapConfig{
			Width:  30,
			Height: 30,
			Seed:   "seed",
		},
	}

	s.Run()
}
