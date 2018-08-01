package main

import "github.com/lemunozm/ascii-arena/pkg/comm"

type RegistryStatus int

const (
	REGISTRY_OK = RegistryStatus(iota)
	REGISTRY_FULL
	REGISTRY_ALREADY_EXISTS
)

type PlayerRegistry struct {
	maxPlayers  int
	pointsToWin int
	players     []*Player
}

func NewPlayerRegistry(maxPlayers int, pointsToWin int) *PlayerRegistry {
	return &PlayerRegistry{
		maxPlayers:  maxPlayers,
		pointsToWin: pointsToWin,
		players:     []*Player{},
	}
}

func (r *PlayerRegistry) Add(character byte, connection *comm.Connection) RegistryStatus {
	if len(r.players) == r.maxPlayers {
		return REGISTRY_FULL
	}

	for _, p := range r.players {
		if p.Character() == character {
			return REGISTRY_ALREADY_EXISTS
		}
	}

	player := NewPlayer(character, connection)
	r.players = append(r.players, player)

	return REGISTRY_OK
}

func (r *PlayerRegistry) Remove(player *Player) error {
	//TODO
	return nil
}

func (r PlayerRegistry) MaxPlayers() int {
	return r.maxPlayers
}

func (r PlayerRegistry) CurrentPlayers() int {
	return len(r.players)
}

func (r PlayerRegistry) Full() bool {
	return r.MaxPlayers() == r.CurrentPlayers()
}

func (r PlayerRegistry) Players() []*Player {
	return r.players
}

func (r PlayerRegistry) HasWinner() bool {
	for _, p := range r.players {
		if p.Points() >= r.pointsToWin {
			return true
		}
	}
	return false
}
