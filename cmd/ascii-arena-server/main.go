package main

import "github.com/lemunozm/ascii-arena/internal/server"

func main() {
	s := server.Server{
		TCPPortGame:       3000,
		TCPPortInfo:       3001,
		MaxPlayers:        1,
		PointsToWin:       1,
		InfoServerEnabled: true,
		Map: server.MapConfig{
			Width:  5,
			Height: 5,
			Seed:   "arena-seed",
		},
	}

	s.Run()
}
