package client

import "github.com/lemunozm/ascii-arena/internal/pkg/comm"
import "github.com/lemunozm/ascii-arena/internal/pkg/logger"

import "strconv"
import "net"
import "fmt"
import "os"
import "io"

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

	file, err := os.Create("log.txt")
	if err == nil {
		logger.SetInfoOutputs([]io.Writer{file})
		logger.SetErrorOutputs([]io.Writer{file})
		logger.SetWarningOutputs([]io.Writer{file})
	}
	return c
}

func (c *Client) Run() {
	connectionInfo := c.connectToInfoServer()
	if connectionInfo != nil {
		gamePort := InfoStage(connectionInfo)
		connectionInfo.Close()

		if gamePort > 0 {
			connectionGame := c.connectToGameServer(gamePort)
			if connectionGame != nil {
				if LogInStage(connectionGame, c.Character) {
					GameStage(connectionGame)
				}
				connectionGame.Close()
			}
		}
	}
}

func (c *Client) connectToInfoServer() *comm.Connection {
	tcpConnectionInfo, err := net.Dial("tcp", c.Host+":"+strconv.Itoa(c.Port))
	if err != nil {
		logger.PrintfError("Create connection to info server => %s", err.Error())
		fmt.Printf("Error to connect to info server at %s:%d\n", c.Host, c.Port)
		return nil
	}
	return comm.NewConnection(tcpConnectionInfo)
}

func (c *Client) connectToGameServer(gamePort int) *comm.Connection {
	tcpConnectionGame, err := net.Dial("tcp", c.Host+":"+strconv.Itoa(gamePort))
	if err != nil {
		logger.PrintfError("Create connection to game server => %s", err.Error())
		fmt.Printf("Error to connect to game server at %s:%d\n", c.Host, gamePort)
		return nil
	}
	return comm.NewConnection(tcpConnectionGame)
}
