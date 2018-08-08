package spatial

import "fmt"

type Vector2 struct {
	X int
	Y int
}

func (v Vector2) GetAdd(v2 Vector2) Vector2 {
	return Vector2{v.X + v2.X, v.Y + v2.Y}
}

func (v Vector2) GetSub(v2 Vector2) Vector2 {
	return Vector2{v.X + v2.X, v.Y + v2.Y}
}

func (v Vector2) IsInside(minX int, maxX int, minY int, maxY int) bool {
	return minX < v.X && v.X < maxX && minY < v.Y && v.Y < maxY
}

func (v Vector2) String() string {
	return fmt.Sprintf("(%d, %d)", v.X, v.Y)
}
