package def

type Wall uint8

const (
	WALL_EMPTY = Wall(iota)
	WALL_BASIC
	WALL_BORDER
)
