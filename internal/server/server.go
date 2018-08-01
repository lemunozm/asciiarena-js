package server

type Server struct {
	TCPPortMatch      int
	TCPPortInfo       int
	MaxPlayers        int
	PointsToWin       int
	MapSeed           string
	InfoServerEnabled bool
}

func (s *Server) Run() {
	matchServer := NewMatchServer(s.TCPPortMatch, s.MaxPlayers, s.PointsToWin, s.MapSeed)
	go matchServer.Run()

	if s.InfoServerEnabled {
		infoServer := NewInfoServer(s.TCPPortInfo, matchServer)
		infoServer.Run()
	}
}
