package client

import "github.com/lemunozm/ascii-arena/internal/pkg/def"
import "github.com/lemunozm/ascii-arena/internal/pkg/comm"
import "github.com/lemunozm/ascii-arena/internal/pkg/logger"

import "strconv"
import "net"
import "fmt"

type Client struct {
	Host      string
	Port      int
	Character byte
}

func NewClient(host string, port int, character byte) *Client {
	c := &Client{
		Host:      host,
		Port:      port,
		Character: character,
	}
	return c
}

func (c *Client) Run() {
	tcpConnectionInfo, err := net.Dial("tcp", c.Host+":"+strconv.Itoa(c.Port))
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

		tcpConnectionMatch, err := net.Dial("tcp", c.Host+":"+strconv.Itoa(serverInfoMessage.Port))
		if err != nil {
			logger.PrintfPanic("Error at create connection => %s", err.Error())
		}
		connectionMatch := comm.NewConnection(tcpConnectionMatch)

		newPlayerMessage := comm.NewPlayerMessage{c.Character}
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

				currentPlayers = len(playersInfoMessage.Players)
			}

			logger.PrintfInfo("%s", "Start game")
			matchInfoMessage := comm.MatchInfoMessage{}
			connectionMatch.Receive(&matchInfoMessage)

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
