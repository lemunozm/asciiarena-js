package match

import "github.com/lemunozm/ascii-arena/internal/pkg/spatial"

type Character struct {
	representation byte
	position       spatial.Vector2
}

func NewCharacter(representation byte, position spatial.Vector2) *Character {
	return &Character{
		representation: representation,
		position:       position,
	}
}

func (c Character) GetRepresentation() byte {
	return c.representation
}

func (c Character) GetPosition() spatial.Vector2 {
	return c.position
}
