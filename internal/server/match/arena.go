package match

type Arena struct {
	arenaMap *Map
}

func NewArena(width int, height int, seed string, characters []byte) *Arena {
	a := &Arena{
		arenaMap: NewMap(width, height, seed),
	}

	return a
}

func (a Arena) GetMap() *Map {
	return a.arenaMap
}
