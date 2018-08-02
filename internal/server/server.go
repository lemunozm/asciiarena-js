package server

type MapConfig struct {
	Width  int
	Height int
	Seed   string
}

type Server struct {
	TCPPortGame       int
	TCPPortInfo       int
	MaxPlayers        int
	PointsToWin       int
	InfoServerEnabled bool
	Map               MapConfig
}

func (s *Server) Run() {
	gameServer := NewGameServer(s.TCPPortGame, s.MaxPlayers, s.PointsToWin, s.Map)
	go gameServer.Run()

	if s.InfoServerEnabled {
		infoServer := NewInfoServer(s.TCPPortInfo, gameServer)
		infoServer.Run()
	}
}
