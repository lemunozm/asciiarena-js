package spatial

type Direction int

const (
	DIRECTION_UP = Direction(iota)
	DIRECTION_RIGHT
	DIRECTION_DOWN
	DIRECTION_LEFT
)

func GetDirectionVector(direction Direction) Vector2 {
	switch direction {
	case DIRECTION_UP:
		return Vector2{0, -1}
	case DIRECTION_RIGHT:
		return Vector2{1, 0}
	case DIRECTION_DOWN:
		return Vector2{0, 1}
	case DIRECTION_LEFT:
		return Vector2{-1, 0}
	default:
		return Vector2{0, 0}
	}
}
