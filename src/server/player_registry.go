package main

import "net"

type PlayerRegistry struct {
	maxPlayers int
	players    []*Player
}

func NewPlayerRegistry(maxPlayers int) *PlayerRegistry {
	return &PlayerRegistry{
		maxPlayers: maxPlayers,
		players:    []*Player{},
	}
}

func (r *PlayerRegistry) Add(character uint8, connection net.Conn) *Player {
	//TODO
	player := NewPlayer(character, connection)
	r.players = append(r.players, player)
	return player
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

func (r PlayerRegistry) Players() []*Player {
	return r.players
}
