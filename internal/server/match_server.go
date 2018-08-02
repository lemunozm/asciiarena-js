package server

import "github.com/lemunozm/ascii-arena/internal/pkg/logger"
import "github.com/lemunozm/ascii-arena/internal/pkg/comm"

import "net"
import "strconv"

type MatchServer struct {
	port         int
	matchManager *MatchManager
}

func NewMatchServer(tcpPort int, maxPlayers int, pointsToWin int, mapSeed string) *MatchServer {
	s := &MatchServer{
		port:         tcpPort,
		matchManager: NewMatchManager(maxPlayers, pointsToWin, mapSeed),
	}

	return s
}

func (s MatchServer) GetPort() int {
	return s.port
}

func (s MatchServer) GetMatchManager() *MatchManager {
	return s.matchManager
}

func (s *MatchServer) Run() {
	address, err := net.ResolveTCPAddr("tcp", ":"+strconv.Itoa(s.port))
	if err != nil {
		logger.PrintfPanic("Error resolving tcp address => %s", err.Error())
	}
	listener, err := net.ListenTCP("tcp", address)
	if err != nil {
		logger.PrintfPanic("Error listening from tcp => %s", err.Error())
	}
	defer listener.Close()

	for {
		tcpConnection, err := listener.AcceptTCP()
		if err != nil {
			logger.PrintfPanic("Error accepting => %s", err.Error())
		}
		connection := comm.NewConnection(tcpConnection)

		s.handlePlayerConnection(connection)
	}
}

func (s *MatchServer) handlePlayerConnection(connection *comm.Connection) {
	s.matchManager.RegisterPlayer(connection)

	if s.matchManager.IsReadyToStartGame() {
		go s.matchManager.StartGame()
	}
}
