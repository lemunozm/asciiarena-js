package main

import "github.com/lemunozm/ascii-arena/pkg/comm"
import "fmt"

type MatchManager struct {
	playerRegistry *PlayerRegistry
	startedMatch   bool
}

func NewMatchManager(maxPlayers int) *MatchManager {
	m := &MatchManager{
		playerRegistry: NewPlayerRegistry(maxPlayers),
		startedMatch:   false,
	}

	return m
}

func (s MatchManager) PlayerRegistry() *PlayerRegistry {
	return s.playerRegistry
}

func (s MatchManager) IsStartedMatch() bool {
	return s.startedMatch
}

func (s MatchManager) IsReadyToStartMatch() bool {
	return !s.IsStartedMatch() && s.playerRegistry.Full()
}

func (s *MatchManager) RegisterPlayer(connection *comm.Connection) {
	var loginStatus comm.LoginStatus
	if s.IsStartedMatch() {
		loginStatus = comm.LOGIN_ERR_STARTED_MATCH
	} else {
		newPlayerMessage := comm.NewPlayerMessage{}
		connection.Receive(&newPlayerMessage)

		status := s.playerRegistry.Add(newPlayerMessage.Character, connection)

		switch status {
		case REGISTRY_OK:
			loginStatus = comm.LOGIN_SUCCESSFUL
		case REGISTRY_ALREADY_EXISTS:
			loginStatus = comm.LOGIN_ERR_CHARACTER_EXISTS
		case REGISTRY_FULL: //teorically, it must not happen
			loginStatus = comm.LOGIN_ERR_FULL_MATCH
		}
	}

	playerLoginStatusMessage := comm.PlayerLoginStatusMessage{loginStatus}
	connection.Send(playerLoginStatusMessage)

	s.notifyPlayers(connection, loginStatus)
}

func (s *MatchManager) notifyPlayers(connection *comm.Connection, loginStatus comm.LoginStatus) {
	characters := make([]byte, s.playerRegistry.CurrentPlayers())
	for i, p := range s.playerRegistry.Players() {
		characters[i] = p.Character()
	}
	playersInfoMessage := comm.PlayersInfoMessage{characters}

	if loginStatus == comm.LOGIN_SUCCESSFUL {
		for _, p := range s.playerRegistry.Players() {
			p.Connection().Send(playersInfoMessage)
		}
	} else {
		connection.Send(playersInfoMessage)
	}
}

func (s *MatchManager) Run() {
	s.startedMatch = true
	fmt.Println("Initializing match!")
	for /* anyone has points to win */ {
		s.initializingMatch()
		s.playingMatch()
	}
	s.startedMatch = false
}

func (s *MatchManager) initializingMatch() {
	//TODO
}

func (s *MatchManager) playingMatch() {
	//TODO
}
