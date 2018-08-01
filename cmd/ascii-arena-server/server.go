package main

type Server struct {
	TCPPortMatch      int
	TCPPortInfo       int
	MaxPlayers        int
	PointsToWin       int
	InfoServerEnabled bool
}

func (s *Server) Run() {
	matchServer := NewMatchServer(s.TCPPortMatch, s.MaxPlayers, s.PointsToWin)
	go matchServer.Run()

	if s.InfoServerEnabled {
		infoServer := NewInfoServer(s.TCPPortInfo, matchServer)
		infoServer.Run()
	}
}
