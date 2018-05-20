package main

func main() {
	server := Server{
		TCPPortMatch:      3000,
		TCPPortInfo:       3001,
		MaxPlayers:        4,
		PointsToWin:       1,
		InfoServerEnabled: true,
	}

	server.Run()
}
