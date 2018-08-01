package main

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

			fmt.Println("Initializing match!")
		}
	}
}
