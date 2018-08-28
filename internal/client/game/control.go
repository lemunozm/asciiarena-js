package game

type Control struct {
	screen *Screen
}

func NewControl(screen *Screen) *Control {
	c := &Control{screen}
	return c
}

func (c *Control) ListenEvents() {
	c.screen.ComputeEvents()
	//TODO
}
