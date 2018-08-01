package main

func main() {
	server := Server{
		TCPPortMatch:      3000,
		TCPPortInfo:       3001,
		MaxPlayers:        1,
		PointsToWin:       1,
		MapSeed:           "example",
		InfoServerEnabled: true,
	}

	server.Run()
}
