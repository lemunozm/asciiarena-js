package match

import "github.com/lemunozm/ascii-arena/internal/pkg/logger"
import "github.com/lemunozm/ascii-arena/internal/pkg/spatial"
import "github.com/lemunozm/ascii-arena/internal/pkg/def"
import "math/rand"
import "time"
import "errors"
import "math"

type Arena struct {
	arenaMap   *Map
	random     *rand.Rand
	characters map[int]*Character
}

func NewArena(width int, height int, seed string, characters []byte) *Arena {
	a := &Arena{
		arenaMap:   NewMap(width, height, seed),
		random:     rand.New(rand.NewSource(time.Now().UnixNano())),
		characters: make(map[int]*Character),
	}

	characterPortion := (width * height) / len(characters)
	minDistanceBetweenCharacters := int(math.Sqrt(float64(characterPortion)))

	for _, c := range characters {
		position, err := a.FindRandomFreeCharacterPosition(a.random, minDistanceBetweenCharacters)
		if err != nil {
			logger.PrintfError("At create initial character position %c: => %s", c, err.Error())
		}

		a.characters[int(c)] = NewCharacter(c, position)
	}

	return a
}

func (a Arena) GetMap() *Map {
	return a.arenaMap
}

func (a Arena) GetCharacters() map[int]*Character {
	return a.characters
}

func (a Arena) FindRandomFreeCharacterPosition(rand *rand.Rand, separation int) (spatial.Vector2, error) {
	mapSize := len(a.arenaMap.GetData())
	mapData := make([]def.Wall, mapSize)
	copy(mapData, a.arenaMap.GetData())

	// Set a square arround the characters where other characters can not be.
	for _, c := range a.characters {
		for y := -separation; y <= separation; y++ {
			for x := -separation; x <= separation; x++ {
				position := c.GetPosition().GetAdd(spatial.Vector2{x, y})
				if position.IsInside(0, a.arenaMap.GetWidth(), 0, a.arenaMap.GetHeight()) {
					mapData[a.arenaMap.GetWidth()*position.Y+position.X] = def.WALL_NO_PLAYER
				}
			}
		}
	}

	// Choose a valid random position
	index := rand.Intn(mapSize)
	for p := 0; p < mapSize && mapData[index] != def.WALL_EMPTY; p++ {
		index = (index + 1) % mapSize
	}

	if mapData[index] == def.WALL_EMPTY {
		return spatial.Vector2{index % a.arenaMap.GetWidth(), index / a.arenaMap.GetWidth()}, nil
	} else {
		return spatial.Vector2{-1, -1}, errors.New("Can not find a free position")
	}
}
