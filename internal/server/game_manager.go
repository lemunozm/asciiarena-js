package server

import "github.com/lemunozm/ascii-arena/internal/server/match"
import "github.com/lemunozm/ascii-arena/internal/pkg/comm"
import "github.com/lemunozm/ascii-arena/internal/pkg/logger"

type GameManager struct {
	playerRegistry *PlayerRegistry
	mapConfig      MapConfig
	startedGame    bool
}

func NewGameManager(maxPlayers int, pointsToWin int, mapConfig MapConfig) *GameManager {
	m := &GameManager{
		playerRegistry: NewPlayerRegistry(maxPlayers, pointsToWin),
		mapConfig:      mapConfig,
		startedGame:    false,
	}

	return m
}

func (s GameManager) GetPlayerRegistry() *PlayerRegistry {
	return s.playerRegistry
}

func (s GameManager) IsGameStarted() bool {
	return s.startedGame
}

func (s GameManager) IsReadyToStartGame() bool {
	return !s.IsGameStarted() && s.playerRegistry.IsFull()
}

func (s *GameManager) RegisterPlayer(connection *comm.Connection) {
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

func (s *GameManager) notifyPlayers(connection *comm.Connection, loginStatus comm.LoginStatus) {
	playersInfoMessage := comm.PlayersInfoMessage{s.playerRegistry.GetCharacters()}

	if loginStatus == comm.LOGIN_SUCCESSFUL {
		s.sendToAllPlayers(playersInfoMessage)
	} else {
		connection.Send(playersInfoMessage)
	}
}

func (s *GameManager) StartGame() {
	s.startedGame = true
	logger.PrintfInfo("Start game")

	for !s.playerRegistry.HasWinner() {
		s.startMatch()
	}

	logger.PrintfInfo("Finish game")
	s.startedGame = false
}

func (s *GameManager) startMatch() {
	logger.PrintfInfo("Start match")

	arena := match.NewArena(s.mapConfig.Width, s.mapConfig.Height, s.mapConfig.Seed, s.playerRegistry.GetCharacters())

	charactersInfo := make([]comm.CharacterInfo, 0, len(arena.GetCharacters()))
	for _, c := range arena.GetCharacters() {
		charactersInfo = append(charactersInfo, comm.CharacterInfo{c.GetRepresentation(), c.GetPosition()})
	}

	matchInfoMessage := comm.MatchInfoMessage{
		Width:      arena.GetMap().GetWidth(),
		Height:     arena.GetMap().GetHeight(),
		MapSeed:    arena.GetMap().GetSeed(),
		MapData:    arena.GetMap().GetData(),
		Characters: charactersInfo,
	}
	s.sendToAllPlayers(matchInfoMessage)

	for true {
		//TODO
	}

	logger.PrintfInfo("Finish match")
}

func (s *GameManager) sendToAllPlayers(message interface{}) {
	for _, p := range s.playerRegistry.GetPlayers() {
		p.GetConnection().Send(message)
	}
}
