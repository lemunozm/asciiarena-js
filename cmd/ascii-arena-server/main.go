package main

import "github.com/lemunozm/ascii-arena/internal/server"

func main() {
	s := server.Server{
		TCPPortGame:       3000,
		TCPPortInfo:       3001,
		MaxPlayers:        1,
		PointsToWin:       1,
		MapSeed:           "match-seed",
		InfoServerEnabled: true,
	}

	s.Run()
}
