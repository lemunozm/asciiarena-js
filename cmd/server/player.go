package main

import "net"

type Player struct {
	character  uint8
	connection net.Conn
}

func NewPlayer(character uint8, connection net.Conn) *Player {
	return &Player{character, connection}
}

func (p Player) Character() uint8 {
	return p.character
}

func (p *Player) Connection() net.Conn {
	return p.connection
}
