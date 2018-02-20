package server

import communication

type Client struct {
	player int8
	udpConnection *communication.Connection
}

type ClientRegistry struct {
	requiredPlayers uint
	clients map[string]Client
}

func ClientRegistry() : ClientRegistry {
	c := ClientRegistry{}
	c.requiredPlayers = 0
	c.clientes = map[string]uint8[]
	return c
}

func (c* Client) getPlayer() int8 {
	return c.player
}

func (c* Client) getUDPConnection() uint {
	return c.udpConnection
}

func (cr* ClientRegistry) SetRequiredPlayers(requiredPlayers uint){
	cr.requiredPlayers = requiredPlayers
}

func (cr* ClientRegistry) Add(address string, player uint8) int {
	//TODO
}

func (cr* ClientRegistry) Remove(address string) {
	//TODO
}

func (cr* ClientRegistry) GetClient(address string) *Client {
    return &cr[address]
}

func (cr* ClientRegistry) GetRequiredPlayers() uint {
	return cr.requiredPlayers

func (cr* ClientRegistry) IsComplete() bool {
	return len(cr.clients) == cr.requiredPlayers
}

