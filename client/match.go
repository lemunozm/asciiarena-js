package client

import "log"
import "github.com/nsf/termbox-go"
import "github.com/lemunozm/ASCIIArena/common/communication"

type Match struct {
	//TODO
}

func NewMatch() *Match {
	//TODO
	m := &Match{}

	err := termbox.Init()
	if err != nil {
		log.Panic("Termbox error: ", err)
	}
	termbox.Flush()

	return m
}

func (m *Match) IsFinished() bool {
	//TODO
	return false
}

func (m *Match) Destroy() {
	termbox.Close()
}

func (m *Match) ComputeFrame(frame *communication.FrameData) {
	//TODO
}
