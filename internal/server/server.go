package server

type Server struct {
	TCPPortGame       int
	TCPPortInfo       int
	MaxPlayers        int
	PointsToWin       int
	MapSeed           string
	InfoServerEnabled bool
}

func (s *Server) Run() {
	gameServer := NewGameServer(s.TCPPortGame, s.MaxPlayers, s.PointsToWin, s.MapSeed)
	go gameServer.Run()

	if s.InfoServerEnabled {
		infoServer := NewInfoServer(s.TCPPortInfo, gameServer)
		infoServer.Run()
	}
}
