package game

import "github.com/lemunozm/ascii-arena/internal/pkg/logger"

import "github.com/gdamore/tcell"
import "os"
import "os/signal"

type Screen struct {
	screen     tcell.Screen
	eventChan  chan tcell.Event
	signalChan chan os.Signal
}

func NewScreen() *Screen {
	screen, err := tcell.NewScreen()
	if err != nil {
		logger.PrintfPanic("Cannot alloc screen: %s", err)
	}

	err = screen.Init()
	if err != nil {
		logger.PrintfPanic("Cannot init screen: %s", err)
	}

	s := &Screen{
		screen:     screen,
		eventChan:  make(chan tcell.Event),
		signalChan: make(chan os.Signal),
	}

	st := tcell.StyleDefault
	st.Background(tcell.ColorBlack)
	st.Foreground(tcell.ColorBlack)
	s.screen.SetStyle(st)
	s.screen.HideCursor()
	s.screen.Clear()

	go func() {
		for {
			event := screen.PollEvent()
			s.eventChan <- event
		}
	}()

	signal.Notify(s.signalChan, os.Interrupt)
	signal.Notify(s.signalChan, os.Kill)

	return s
}

func (s *Screen) GetInternal() tcell.Screen {
	return s.screen
}

func (s *Screen) Draw() {
	s.screen.Show()
}

func (s *Screen) ComputeEvents() tcell.Key {
	select {
	case event := <-s.eventChan:
		switch ev := event.(type) {
		case *tcell.EventKey:
			switch ev.Key() {
			case tcell.KeyCtrlC:
				logger.PrintfInfo("Forced exit by user")
				os.Exit(1)
			default:
				return ev.Key()
			}
		}

	case <-s.signalChan:
		logger.PrintfWarning("Forced exit by signals")
		os.Exit(1)

	default:
	}

	return tcell.KeyNUL
}

func (s *Screen) DestroyScreen() {
	s.screen.Fini()
}
