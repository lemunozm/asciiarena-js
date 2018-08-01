package main

import "github.com/lemunozm/ascii-arena/pkg/comm"

type Player struct {
	character  byte
	connection *comm.Connection
	points     int
}

func NewPlayer(character uint8, connection *comm.Connection) *Player {
	return &Player{
		character:  character,
		connection: connection,
		points:     0,
	}
}

func (p Player) Character() uint8 {
	return p.character
}

func (p Player) Connection() *comm.Connection {
	return p.connection
}

func (p *Player) AddPoints(points int) int {
	p.points += points
	return p.points
}

func (p *Player) ResetPoints() {
	p.points = 0
}

func (p Player) Points() int {
	return p.points
}
