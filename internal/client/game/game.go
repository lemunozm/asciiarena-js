package game

import "github.com/lemunozm/ascii-arena/internal/pkg/def"

type Game struct {
	render *Render
}

func NewGame(render *Render) *Game {
	g := &Game{render}
	return g
}

func (g *Game) LoadMap(width int, height int, data []def.Wall) {
	//TODO
}

func (g *Game) LoadCharacters() {
	//TODO
}

func (g *Game) Display() {
	//TODO
}

func (g *Game) DisplayCountdown(countdown float32) {
	//TODO
	for true {
	}
}
