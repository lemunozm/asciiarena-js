package match

import "hash/crc64"
import "math/rand"

type Map struct {
	width  int
	height int
	seed   string
}

func NewMap(width int, height int, seed string) *Map {
	m := &Map{
		width:  width,
		height: height,
		seed:   seed,
	}

	crc64.Checksum([]byte(seed), crc64.MakeTable(crc64.ECMA))
	//TODO (generate map)
	return m
}

func (m Map) GetWidth() int {
	return m.width
}

func (m Map) GetHeight() int {
	return m.height
}

func (m Map) GetSeed() string {
	return m.seed
}

func (m *Map) ComputePlayerOrigins(players []uint8, rand *rand.Rand) {
	//TODO
}
