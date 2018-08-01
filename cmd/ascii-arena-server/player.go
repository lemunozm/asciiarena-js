package main

import "github.com/lemunozm/ascii-arena/pkg/comm"

type Player struct {
	character  byte
	connection *comm.Connection
}

func NewPlayer(character uint8, connection *comm.Connection) *Player {
	return &Player{character, connection}
}

func (p Player) Character() uint8 {
	return p.character
}

func (p Player) Connection() *comm.Connection {
	return p.connection
}
