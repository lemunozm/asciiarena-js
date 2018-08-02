package match

import "hash/crc64"
import "math/rand"
import "fmt"

type Wall uint8

const (
	WALL_EMPTY = Wall(iota)
	WALL_BASIC
	WALL_BORDER
)

type Map struct {
	width  int
	height int
	seed   string
	table  []Wall
}

func NewMap(width int, height int, seed string) *Map {
	m := &Map{
		width:  width,
		height: height,
		seed:   seed,
		table:  make([]Wall, width*height),
	}

	m.clean()
	m.buildBorder()
	fmt.Println(m.table)
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

func (m Map) getBox(x int, y int) Wall {
	return m.table[m.width*y+x]
}

func (m *Map) setBox(x int, y int, box Wall) {
	m.table[m.width*y+x] = box
}

func (m *Map) ComputePlayerOrigins(players []Wall, rand *rand.Rand) {
	//TODO
}

func (m *Map) clean() {
	for i := 0; i < m.width*m.height; i++ {
		m.table[i] = WALL_EMPTY
	}
}

func (m *Map) buildBorder() {
	for x := 0; x < m.width; x++ {
		m.setBox(x, 0, WALL_BORDER)
	}
	for x := 0; x < m.width; x++ {
		m.setBox(x, m.height-1, WALL_BORDER)
	}
	for y := 1; y < m.height-1; y++ {
		m.setBox(0, y, WALL_BORDER)
	}
	for y := 1; y < m.height-1; y++ {
		m.setBox(m.width-1, y, WALL_BORDER)
	}
}

func (m *Map) generate() {
	crc64.Checksum([]byte(m.seed), crc64.MakeTable(crc64.ECMA))
}
