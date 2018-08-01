package match

type Arena struct {
	arenaMap *Map
}

func NewArena(width int, height int, seed string) *Arena {
	a := &Arena{
		arenaMap: NewMap(width, height, seed),
	}

	return a
}

func (a Arena) Map() *Map {
	return a.arenaMap
}
