package main

import "github.com/lemunozm/ascii-arena/internal/server"

func main() {
	s := server.Server{
		TCPPortMatch:      3000,
		TCPPortInfo:       3001,
		MaxPlayers:        1,
		PointsToWin:       1,
		MapSeed:           "example",
		InfoServerEnabled: true,
	}

	s.Run()
}
