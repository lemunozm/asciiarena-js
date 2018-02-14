package client

import "fmt"
import "net"
import "log"
import "strconv"
import "github.com/lemunozm/ASCIIArena/common"
import "github.com/lemunozm/ASCIIArena/common/communication"

type Client struct {
}

func NewClient() *Client {
	c := &Client{}
	return c
}

func (c *Client) Run(host string, port uint) {

	tcpSocket, err := net.Dial("tcp", host+":"+strconv.FormatUint(uint64(port), 10))
	if err != nil {
		log.Panic("Connection error: ", err)
	}
	defer tcpSocket.Close()
	fmt.Printf("Connect to server on: %s:%d\n", host, port)

	connection := communication.NewConnection(tcpSocket)
	connection.RegisterRecvData(communication.VersionCheckedData{}, c.RecvVersionCheckedData)
	connection.RegisterRecvData(communication.LoadMatchData{}, c.RecvLoadMatchData)

	versionData := communication.VersionData{common.GetVersion()}
	connection.Send(&versionData)
	connection.ListenLoop()
}

func (c *Client) RecvVersionCheckedData(data interface{}, connection *communication.Connection) {
	if versionCheckedData, ok := data.(communication.VersionCheckedData); ok {
		from := connection.GetSocket().RemoteAddr()
		fmt.Println("Recv VersionCheckedData:", versionCheckedData, "from:", from)
	}
}

func (c *Client) RecvLoadMatchData(data interface{}, connection *communication.Connection) {
	if LoadMatch, ok := data.(communication.LoadMatchData); ok {
		from := connection.GetSocket().RemoteAddr()
		fmt.Println("Recv InitMatchData:", LoadMatch, "from:", from)

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
