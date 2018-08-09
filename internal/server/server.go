package server

type MapConfig struct {
	Width  int
	Height int
	Seed   string
}

type Server struct {
	GameTCPPort int
	InfoTCPPort int
	Players     int
	PointsToWin int
	Map         MapConfig
}

func (s *Server) Run() {
	gameServer := NewGameServer(s.GameTCPPort, s.Players, s.PointsToWin, s.Map)
	go gameServer.Run()

	infoServer := NewInfoServer(s.InfoTCPPort, gameServer)
	infoServer.Run()
}
