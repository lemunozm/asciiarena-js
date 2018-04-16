package server

import "github.com/lemunozm/ASCIIArena/common/communication"

type RegisterStatus uint

const (
	CLIENT_REGISTRY_OK RegisterStatus = iota
	CLIENT_REGISTRY_PLAYER_LIMIT
	CLIENT_REGISTRY_ALREADY_EXISTS
)

type Client struct {
	player        int8
	udpConnection *communication.Connection
}

type ClientRegistry struct {
	requiredPlayers uint
	clients         map[string]Client
}

func ClientRegistry(requiredPlayers uint) ClientRegistry {
	c := ClientRegistry{}
	c.requiredPlayers = 0
	c.clientes = map[string]Client{}
	return c
}

func (c *Client) getPlayer() int8 {
	return c.player
}

func (c *Client) getUDPConnection() uint {
	return c.udpConnection
}

func (cr *ClientRegistry) SetRequiredPlayers(requiredPlayers uint) {
	cr.requiredPlayers = requiredPlayers
}

func (cr *ClientRegistry) Add(address string, player uint8) RegisterStatus {
	if IsComplete() {
		return CLIENT_REGISTRY_PLAYER_LIMIT
	}

	if clients[address] {
		return CLIENT_REGISTRY_ALREADY_EXISTS
	}

	clients[address] = Client{player, nil}
	return CLIENT_REGISTRY_OK
}

func (cr *ClientRegistry) Remove(address string) {
	//TODO
}

func (cr *ClientRegistry) GetClient(address string) *Client {
	return &cr[address]
}

func (cr *ClientRegistry) GetRequiredPlayers() uint {
	return cr.requiredPlayers
}

func (cr *ClientRegistry) IsComplete() bool {
	return len(cr.clients) == cr.requiredPlayers
}

func (cr *ClientRegistry) Clear() {
	//TODO
}
