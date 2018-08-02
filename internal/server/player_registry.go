package server

import "github.com/lemunozm/ascii-arena/internal/pkg/comm"

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
		if p.GetCharacter() == character {
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

func (r PlayerRegistry) GetMaxPlayers() int {
	return r.maxPlayers
}

func (r PlayerRegistry) GetCurrentPlayers() int {
	return len(r.players)
}

func (r PlayerRegistry) GetCharacters() []byte {
	characters := make([]byte, r.GetCurrentPlayers())
	for i, p := range r.players {
		characters[i] = p.GetCharacter()
	}
	return characters
}

func (r PlayerRegistry) IsFull() bool {
	return r.GetMaxPlayers() == r.GetCurrentPlayers()
}

func (r PlayerRegistry) GetPlayers() []*Player {
	return r.players
}

func (r PlayerRegistry) HasWinner() bool {
	for _, p := range r.players {
		if p.GetPoints() >= r.pointsToWin {
			return true
		}
	}
	return false
}
