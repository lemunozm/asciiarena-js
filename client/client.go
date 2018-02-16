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
	connection.RegisterRecvData(communication.VersionCheckedData{}, c.RecvVersionCheckedData)
	connection.RegisterRecvData(communication.LogInStatusData{}, c.RecvLogInStatusData)
	connection.RegisterRecvData(communication.LoadMatchData{}, c.RecvLoadMatchData)

	versionData := communication.VersionData{common.GetVersion()}
	connection.Send(versionData)
	var versionCheckedData communication.VersionCheckedData
	connection.Receive(&versionCheckedData)
	connection.Send(communication.LogInData{})
	var logInStatusData communication.LogInStatusData
	connection.Receive(&logInStatusData)
	for {
		var playerConnectionData communication.PlayerConnectionData
		connection.Receive(&playerConnectionData)
	}
	var loadMatchData communication.LoadMatchData
	connection.Receive(&loadMatchData)

	connection.ListenLoop()
}

func (c *Client) RecvVersionCheckedData(data interface{}, connection *communication.Connection) {
	if _, ok := data.(communication.VersionCheckedData); ok {
		connection.Send(communication.LogInData{})
	}
}

func (c *Client) RecvLogInStatusData(data interface{}, connection *communication.Connection) {
	if _, ok := data.(communication.LogInStatusData); ok {
	}
}

func (c *Client) RecvLoadMatchData(data interface{}, connection *communication.Connection) {
	if _, ok := data.(communication.LoadMatchData); ok {

		/*udpSocket, err := net.Dial("udp", "host:port")
		if err != nil {
			log.Panic("Connection error: ", err)
		}
		connection := communication.NewConnection(udpSocket)
		connection.RegisterReceiverData(communication.StateData{}, s.StateDataReceived)
		go connection.ListenLoop()*/
	}
}

/*func (c *Client) RecvStateData(data interface{}, connection *communication.Connection) {
	if state, ok := data.(communication.StateData); ok {
		from := connection.GetSocket().RemoteAddr()
		fmt.Println("Recv State:", state, "from:", from)
	}
}*/
