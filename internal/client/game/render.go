package game

type Render struct {
	screen *Screen
}

func NewRender(screen *Screen) *Render {
	r := &Render{screen}
	return r
}

func (r *Render) Map(width int, height int, data int) {

}

func (r *Render) PlayerPanel() {

}
