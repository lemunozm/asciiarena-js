package client

import "github.com/lemunozm/ascii-arena/internal/pkg/comm"
import gamepkg "github.com/lemunozm/ascii-arena/internal/client/game"

func GameStage(connection *comm.Connection) {
	screen := gamepkg.NewScreen()
	render := gamepkg.NewRender(screen)
	game := gamepkg.NewGame(render)

	control := gamepkg.NewControl(screen)
	go control.ListenEvents()

	for true {
		matchInfoMessage := comm.MatchInfoMessage{}
		connection.Receive(&matchInfoMessage)

		if matchInfoMessage.GameEnd {
			//store information about the points
			break
		}

		game.LoadMap(matchInfoMessage.Width, matchInfoMessage.Height, matchInfoMessage.MapData)
		game.LoadCharacters() // matchInfoMessage.Characters) //load points
		game.Display()
		game.DisplayCountdown(matchInfoMessage.Countdown)

		/*for true {
			frameMessage := comm.FrameMessage{}
			connection.Receive(&frameMessage)

			if frameMessage.MatchEnd {
				break
			}

			game.Update()
			game.Display()

			userAction = control.GetPlayerAction()
			if(userAction == USER_ACTION_EXIT) {
				return
			}

			playerActionMessage := comm.PlayerActionMessage{userAction}
			connection.Send(playerActionMessage)
		}*/
	}

	screen.DestroyScreen()
	//process end game
}

/* func drawWall(wallCode def.Wall) byte {
	switch wallCode {
	case def.WALL_EMPTY:
		return ' '
	case def.WALL_BASIC:
		return 'x'
	case def.WALL_BORDER:
		return 'X'
	}
	return '?'
} */

/*
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
*/
