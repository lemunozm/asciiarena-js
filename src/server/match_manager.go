package main

type MatchManager struct {
	playerRegistry *PlayerRegistry
}

func NewMatchManager(maxPlayers int) *MatchManager {
	m := &MatchManager{
		playerRegistry: NewPlayerRegistry(maxPlayers),
	}

	return m
}

func (s MatchManager) PlayerRegistry() *PlayerRegistry {
	return s.playerRegistry
}

func (s *MatchManager) Run() {
	for /* anyone has points to win */ {
		s.initializingMatch()
		s.playingMatch()
	}
}

func (s *MatchManager) initializingMatch() {
	//TODO
}

func (s *MatchManager) playingMatch() {
	//TODO
}
