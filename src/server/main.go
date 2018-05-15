package main

func main() {
	// values from cli
	serverConfiguration := MatchServerConfiguration{
		TCPPort:           3000,
		TCPPortInfo:       3001,
		MaxPlayers:        4,
		PointsToWin:       1,
		InfoServerEnabled: true,
	}

	// running
	matchServer := NewMatchServer(serverConfiguration)
	matchServer.Run()
}
