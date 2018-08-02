package server

import "github.com/lemunozm/ascii-arena/internal/pkg/comm"

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

func (p Player) GetCharacter() uint8 {
	return p.character
}

func (p Player) GetConnection() *comm.Connection {
	return p.connection
}

func (p Player) GetPoints() int {
	return p.points
}

func (p *Player) AddPoints(points int) int {
	p.points += points
	return p.points
}

func (p *Player) ResetPoints() {
	p.points = 0
}
