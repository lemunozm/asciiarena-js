package client

import "github.com/lemunozm/ascii-arena/internal/pkg/def"
import "github.com/lemunozm/ascii-arena/internal/pkg/comm"
import "fmt"

func GameStage(connection *comm.Connection) {

	matchInfoMessage := comm.MatchInfoMessage{}
	connection.Receive(&matchInfoMessage)

	for y := 0; y < matchInfoMessage.Height; y++ {
		for x := 0; x < matchInfoMessage.Width; x++ {
			drawing := drawWall(matchInfoMessage.MapData[matchInfoMessage.Width*y+x])
			for _, c := range matchInfoMessage.Characters {
				if x == c.Position.X && y == c.Position.Y {
					drawing = c.Representation
				}
			}

			fmt.Printf("%c ", drawing)
		}
		fmt.Printf("\n")
	}
}

func drawWall(wallCode def.Wall) byte {
	switch wallCode {
	case def.WALL_EMPTY:
		return ' '
	case def.WALL_BASIC:
		return 'x'
	case def.WALL_BORDER:
		return 'X'
	}
	return '?'
}
