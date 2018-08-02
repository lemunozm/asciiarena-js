package server

import "github.com/lemunozm/ascii-arena/internal/pkg/logger"
import "github.com/lemunozm/ascii-arena/internal/pkg/comm"

import "net"
import "strconv"

type GameServer struct {
	port        int
	gameManager *GameManager
}

func NewGameServer(tcpPort int, maxPlayers int, pointsToWin int, mapConfig MapConfig) *GameServer {
	s := &GameServer{
		port:        tcpPort,
		gameManager: NewGameManager(maxPlayers, pointsToWin, mapConfig),
	}

	return s
}

func (s GameServer) GetPort() int {
	return s.port
}

func (s GameServer) GetGameManager() *GameManager {
	return s.gameManager
}

func (s *GameServer) Run() {
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

func (s *GameServer) handlePlayerConnection(connection *comm.Connection) {
	s.gameManager.RegisterPlayer(connection)

	if s.gameManager.IsReadyToStartGame() {
		go s.gameManager.StartGame()
	}
}
