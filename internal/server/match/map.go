package match

import "github.com/lemunozm/ascii-arena/internal/pkg/spatial"
import "github.com/lemunozm/ascii-arena/internal/pkg/def"
import "hash/crc64"

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
	m.generate()
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

func (m Map) GetBox(position spatial.Vector2) def.Wall { //To Vector
	return m.data[m.width*position.Y+position.X]
}

func (m *Map) SetBox(position spatial.Vector2, box def.Wall) {
	m.data[m.width*position.Y+position.X] = box
}

func (m *Map) clean() {
	for i := 0; i < m.width*m.height; i++ {
		m.data[i] = def.WALL_EMPTY
	}
}

func (m *Map) buildBorder() {
	for x := 0; x < m.width; x++ {
		m.SetBox(spatial.Vector2{x, 0}, def.WALL_BORDER) //comprobar la inicializacion rapida del vector
	}
	for x := 0; x < m.width; x++ {
		m.SetBox(spatial.Vector2{x, m.height - 1}, def.WALL_BORDER)
	}
	for y := 1; y < m.height-1; y++ {
		m.SetBox(spatial.Vector2{0, y}, def.WALL_BORDER)
	}
	for y := 1; y < m.height-1; y++ {
		m.SetBox(spatial.Vector2{m.width - 1, y}, def.WALL_BORDER)
	}
}

func (m *Map) generate() {
	crc64.Checksum([]byte(m.seed), crc64.MakeTable(crc64.ECMA))
	//TODO
}
