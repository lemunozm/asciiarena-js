package client

import "net"
import "log"
import "strconv"
import "github.com/lemunozm/ASCIIArena/common"
import "github.com/lemunozm/ASCIIArena/common/communication"

type Client struct {
	host          string
	remoteTCPPort string
	localUDPPort  string
}

func NewClient(host string, remoteTCPPort uint, localUDPPort uint) *Client {
	c := &Client{}
	c.host = host
	c.remoteTCPPort = strconv.FormatUint(uint64(remoteTCPPort), 10)
	c.localUDPPort = strconv.FormatUint(uint64(localUDPPort), 10)
	return c
}

func (c *Client) Run() {

	tcpSocket, err := net.Dial("tcp", c.host+":"+c.remoteTCPPort)
	if err != nil {
		log.Panic("Connection error: ", err)
	}
	defer tcpSocket.Close()

	connection := communication.NewConnection(tcpSocket, true)

	if c.checkVersion(connection) {
		c.logIn(connection)
	}

	/*
		connection.Send(communication.LogInData{})
		var logInStatusData communication.LogInStatusData
		connection.Receive(&logInStatusData)
		for {
			var playerConnectionData communication.PlayerConnectionData
			connection.Receive(&playerConnectionData)
		}
		var loadMatchData communication.LoadMatchData
		connection.Receive(&loadMatchData)
	*/
}

func (c *Client) checkVersion(connection *communication.Connection) bool {
	versionData := communication.VersionData{common.GetVersion()}
	connection.Send(versionData)

	var versionCheckedData communication.VersionCheckedData
	connection.Receive(&versionCheckedData)

	return versionCheckedData.Validation
}

func (c *Client) logIn(connection *communication.Connection) {
	logInData := communication.LogInData{'A'}
	connection.Send(logInData)

	var logInStatusData communication.LogInStatusData
	connection.Receive(&logInStatusData)
}
