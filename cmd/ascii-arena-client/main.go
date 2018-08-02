package main

import "github.com/lemunozm/ascii-arena/internal/pkg/def"
import "github.com/lemunozm/ascii-arena/internal/pkg/comm"
import "github.com/lemunozm/ascii-arena/internal/pkg/logger"

import "strconv"
import "net"
import "os"
import "fmt"

func main() {
	if len(os.Args) < 2 {
		fmt.Println("Please, choose a valid character.")
		return
	}

	character := os.Args[1][0]

	tcpConnectionInfo, err := net.Dial("tcp", "127.0.0.1:3001")
	if err != nil {
		logger.PrintfPanic("Error at create connection => %s", err.Error())
	}
	connectionInfo := comm.NewConnection(tcpConnectionInfo)

	versionMessage := comm.VersionMessage{"0.1.0"}
	connectionInfo.Send(versionMessage)

	checkedVersionMessage := comm.CheckedVersionMessage{}
	connectionInfo.Receive(&checkedVersionMessage)

	if checkedVersionMessage.Validation {
		serverInfoMessage := comm.ServerInfoMessage{}
		connectionInfo.Receive(&serverInfoMessage)

		tcpConnectionMatch, err := net.Dial("tcp", "127.0.0.1:"+strconv.Itoa(serverInfoMessage.Port))
		if err != nil {
			logger.PrintfPanic("Error at create connection => %s", err.Error())
		}
		connectionMatch := comm.NewConnection(tcpConnectionMatch)

		newPlayerMessage := comm.NewPlayerMessage{character}
		connectionMatch.Send(&newPlayerMessage)

		playerLoginStatusMessage := comm.PlayerLoginStatusMessage{}
		connectionMatch.Receive(&playerLoginStatusMessage)

		if playerLoginStatusMessage.LoginStatus == comm.LOGIN_SUCCESSFUL {
			currentPlayers := serverInfoMessage.CurrentPlayers
			for currentPlayers < serverInfoMessage.MaxPlayers {
				playersInfoMessage := comm.PlayersInfoMessage{}
				if !connectionMatch.Receive(&playersInfoMessage) {
					return
				}

				currentPlayers = len(playersInfoMessage.Characters)
			}

			logger.PrintfInfo("%s", "Start game")
			matchInfoMessage := comm.MatchInfoMessage{}
			connectionMatch.Receive(&matchInfoMessage)

			for y := 0; y < matchInfoMessage.Height; y++ {
				for x := 0; x < matchInfoMessage.Width; x++ {
					fmt.Printf("%c ", drawWall(matchInfoMessage.MapData[matchInfoMessage.Width*y+x]))
				}
				fmt.Printf("\n")
			}
		}
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
