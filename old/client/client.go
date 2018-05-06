package client

import "fmt"
import "net"
import "log"
import "strconv"
import "time"
import "github.com/lemunozm/ASCIIArena/common"
import "github.com/lemunozm/ASCIIArena/common/communication"

type Client struct {
	host          string
	localUDPPort  uint
	remoteTCPPort uint
	tcpConnection *communication.Connection
	udpConnection *communication.Connection
	frameId       uint
}

func NewClient(host string, remoteTCPPort uint, localUDPPort uint) *Client {

	c := &Client{}
	c.host = host
	c.localUDPPort = localUDPPort
	c.remoteTCPPort = remoteTCPPort
	c.frameId = 0
	return c
}

func (c *Client) Run() {
	playerController := NewPlayerController( /* yaml? */ )
	// configurate control?

	tcpSocket, err := net.Dial("tcp", c.host+":"+strconv.FormatUint(uint64(c.remoteTCPPort), 10))
	if err != nil {
		log.Panic("Connection error: ", err)
	}
	c.tcpConnection = communication.NewConnection(tcpSocket)

	if c.checkVersion() {
		player := int8('A')
		logInStatus := c.logIn(player)
		// check logInStatus and repeat request player name if it fails
		for {
			match := c.waitingMatch(&logInStatus)
			for !match.IsFinished() {
				c.userAction(playerController)
			}
			match.Destroy()
		}
		c.udpConnection.GetSocket().Close()
	}
	c.tcpConnection.GetSocket().Close()
}

func (c *Client) checkVersion() bool {
	versionData := communication.VersionData{common.GetVersion()}
	c.tcpConnection.Send(versionData)

	var versionCheckedData communication.VersionCheckedData
	c.tcpConnection.Receive(&versionCheckedData)

	return versionCheckedData.Validation
}

func (c *Client) logIn(player int8) communication.LogInStatusData {
	logInData := communication.LogInData{player, uint16(c.localUDPPort)}
	c.tcpConnection.Send(logInData)

	var logInStatusData communication.LogInStatusData
	c.tcpConnection.Receive(&logInStatusData)

	localAddress, err := net.ResolveUDPAddr("udp", ":"+strconv.FormatUint(uint64(c.localUDPPort), 10))
	if err != nil {
		log.Panic("Connection error: ", err)
	}
	serverAddress, err := net.ResolveUDPAddr("udp", c.host+":"+strconv.FormatUint(uint64(logInStatusData.ServerUdpPort), 10))
	if err != nil {
		log.Panic("Connection error: ", err)
	}
	udpSocket, err := net.DialUDP("udp", localAddress, serverAddress)
	if err != nil {
		log.Panic("Connection error: ", err)
	}
	c.udpConnection = communication.NewConnection(udpSocket)

	return logInStatusData
}

func (c *Client) waitingMatch(logInStatus *communication.LogInStatusData) *Match {
	var players []int8 = logInStatus.RegisteredPlayers
	for len(players) < int(logInStatus.RequiredPlayers) {
		var playerConnectionData communication.PlayerConnectionData
		c.tcpConnection.Receive(&playerConnectionData)

		if playerConnectionData.ConnectionState == true {
			players = append(players, playerConnectionData.Player)
		} else {
			for i := range players {
				if players[i] == playerConnectionData.Player {
					players = append(players[:i], players[i+1:]...)
					break
				}
			}
		}
	}

	var loadMatchData communication.LoadMatchData
	c.tcpConnection.Receive(&loadMatchData)

	return c.initMatch(&loadMatchData)
}

func (c *Client) initMatch(loadMatchData *communication.LoadMatchData) *Match {
	match := NewMatch()
	go c.listenFrames(match)
	time.Sleep(time.Duration(loadMatchData.MillisecondsToStart) * time.Millisecond)
	return match
}

func (c *Client) listenFrames(match *Match) {
	c.frameId = 0
	for !match.IsFinished() {
		var frameData communication.FrameData
		c.udpConnection.Receive(&frameData)

		match.ComputeFrame(&frameData)
		// render
		c.frameId = uint(frameData.FrameId)
	}
}

func (c *Client) userAction(playerController *PlayerController) {
	//check user input.
	action := playerController.ProcessInput()
	playerAction := communication.PlayerActionData{uint32(c.frameId), action}
	c.tcpConnection.Send(playerAction)
}
