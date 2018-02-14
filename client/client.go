package client

import "fmt"
import "net"
import "log"
import "github.com/lemunozm/ASCIIArena/common"
import "github.com/lemunozm/ASCIIArena/common/communication"

type Client struct {
	network communication.NetworkManager
}

func NewClient() *Client {
	c := &Client{}
	return c
}

func (c *Client) Run(host string, port uint) {

	tcpSocket, err := net.Dial("tcp", host+":"+port)
	if err != nil {
		log.Panic("Connection error: ", err)
	}
	defer tcpSocket.Close()
	fmt.Printf("Connect to server on: %s:%d\n", host, port)

	connection := communication.NewConnection(tcpSocket)
	connection.RegisterReceiverData(communication.VersionCheckedData{}, s.VersionCheckedDataReceived)
	connection.RegisterReceiverData(communication.InitMatchData{}, s.InitMatchDataReceived)

	versionData := communication.VersionData{common.GetVersion()}
	connection.Send(&versionData)
	connection.ListenLoop()
}

func (c *Client) VersionCheckedDataReceived(data interface{}, connection *communication.Connection) {
	if versionCheckedData, ok := data.(communication.VersionCheckedData); ok {
		fmt.Println("Recv VersionCheckedData:", versionCheckedData, "from:", from)
	}
}

func (c *Client) InitMatchDataReceived(data interface{}, connection *communication.Connection) {
	if initMatch, ok := data.(communication.InitMatchData); ok {
		fmt.Println("Recv InitMatchData:", initMatch, "from:", from)

		/*udpSocket, err := net.Dial("udp", "host:port")
		if err != nil {
			log.Panic("Connection error: ", err)
		}
		connection := communication.NewConnection(udpSocket)
		connection.RegisterReceiverData(communication.StateData{}, s.StateDataReceived)
		go connection.ListenLoop()*/
	}
}

func (c *Client) StateDataReceived(data interface{}, connection *communication.Connection) {
	if state, ok := data.(communication.StateData); ok {
		fmt.Println("Recv State:", state, "from:", from)
	}
}
