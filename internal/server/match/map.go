package match

import "github.com/lemunozm/ascii-arena/internal/pkg/def"
import "hash/crc64"
import "math/rand"

type Map struct {
	width  int
	height int
	seed   string
	data   []def.Wall
}

func NewMap(width int, height int, seed string) *Map {
	m := &Map{
		width:  width,
		height: height,
		seed:   seed,
		data:   make([]def.Wall, width*height),
	}

	m.clean()
	m.buildBorder()
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

func (m Map) GetData() []def.Wall {
	return m.data
}

func (m Map) getBox(x int, y int) def.Wall {
	return m.data[m.width*y+x]
}

func (m *Map) setBox(x int, y int, box def.Wall) {
	m.data[m.width*y+x] = box
}

func (m *Map) ComputePlayerOrigins(players []def.Wall, rand *rand.Rand) {
	//TODO
}

func (m *Map) clean() {
	for i := 0; i < m.width*m.height; i++ {
		m.data[i] = def.WALL_EMPTY
	}
}

func (m *Map) buildBorder() {
	for x := 0; x < m.width; x++ {
		m.setBox(x, 0, def.WALL_BORDER)
	}
	for x := 0; x < m.width; x++ {
		m.setBox(x, m.height-1, def.WALL_BORDER)
	}
	for y := 1; y < m.height-1; y++ {
		m.setBox(0, y, def.WALL_BORDER)
	}
	for y := 1; y < m.height-1; y++ {
		m.setBox(m.width-1, y, def.WALL_BORDER)
	}
}

func (m *Map) generate() {
	crc64.Checksum([]byte(m.seed), crc64.MakeTable(crc64.ECMA))
}
