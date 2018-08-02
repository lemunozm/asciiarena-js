package server

import "github.com/lemunozm/ascii-arena/internal/server/match"
import "github.com/lemunozm/ascii-arena/internal/pkg/comm"
import "github.com/lemunozm/ascii-arena/internal/pkg/logger"

type MatchManager struct {
	playerRegistry *PlayerRegistry
	mapSeed        string
	startedGame    bool
}

func NewMatchManager(maxPlayers int, pointsToWin int, mapSeed string) *MatchManager {
	m := &MatchManager{
		playerRegistry: NewPlayerRegistry(maxPlayers, pointsToWin),
		mapSeed:        mapSeed,
		startedGame:    false,
	}

	return m
}

func (s MatchManager) GetPlayerRegistry() *PlayerRegistry {
	return s.playerRegistry
}

func (s MatchManager) IsGameStarted() bool {
	return s.startedGame
}

func (s MatchManager) IsReadyToStartGame() bool {
	return !s.IsGameStarted() && s.playerRegistry.IsFull()
}

func (s *MatchManager) RegisterPlayer(connection *comm.Connection) {
	var loginStatus comm.LoginStatus
	if s.IsGameStarted() {
		loginStatus = comm.LOGIN_ERR_GAME_STARTED
		logger.PrintfInfo("Login error: game started")
	} else {
		newPlayerMessage := comm.NewPlayerMessage{}
		connection.Receive(&newPlayerMessage)

		status := s.playerRegistry.Add(newPlayerMessage.Character, connection)

		switch status {
		case REGISTRY_OK:
			loginStatus = comm.LOGIN_SUCCESSFUL
			logger.PrintfInfo("Login succesful (player %c)", newPlayerMessage.Character)
		case REGISTRY_ALREADY_EXISTS:
			loginStatus = comm.LOGIN_ERR_CHARACTER_EXISTS
			logger.PrintfInfo("Login error (player %c): character exists", newPlayerMessage.Character)
		case REGISTRY_FULL: //teorically, it must not happen
			loginStatus = comm.LOGIN_ERR_FULL_PLAYERS
			logger.PrintfInfo("Login error (player %c): full players", newPlayerMessage.Character)
		}
	}

	playerLoginStatusMessage := comm.PlayerLoginStatusMessage{loginStatus}
	connection.Send(playerLoginStatusMessage)

	s.notifyPlayers(connection, loginStatus)
}

func (s *MatchManager) notifyPlayers(connection *comm.Connection, loginStatus comm.LoginStatus) {
	playersInfoMessage := comm.PlayersInfoMessage{s.playerRegistry.GetCharacters()}

	if loginStatus == comm.LOGIN_SUCCESSFUL {
		for _, p := range s.playerRegistry.GetPlayers() {
			p.GetConnection().Send(playersInfoMessage)
		}
	} else {
		connection.Send(playersInfoMessage)
	}
}

func (s *MatchManager) StartGame() {
	s.startedGame = true
	logger.PrintfInfo("Start game")

	for !s.playerRegistry.HasWinner() {
		s.startMatch()
	}

	logger.PrintfInfo("Finish game")
	s.startedGame = false
}

func (s *MatchManager) startMatch() {
	//TODO
	logger.PrintfInfo("Start match")

	match.NewArena(32, 32, s.mapSeed, s.playerRegistry.GetCharacters())
	// send to clients

	for true {
	}
	logger.PrintfInfo("Finish match")
}
