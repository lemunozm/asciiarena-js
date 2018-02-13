package client

import "fmt"
import "net"
import "github.com/lemunozm/ASCIIArena/common"
import "github.com/lemunozm/ASCIIArena/common/communication"

type Client struct {
	connection *communication.Connection
}

func NewClient(host string, port uint) *Client {
	fmt.Printf("Connect to server on: %s:%d\n", host, port)

	connection := communication.NewClientConnection(host, port)	
	return &Client{connection}
}

func (c *Client) Run() {
	c.connection.RegisterReceiverData(communication.VersionCheckedData{}, c.VersionCheckedDataReceived, communucation.UDP)

	versionData := communication.VersionData{common.GetVersion()}
	c.SendVersionData(&versionData, c.connection.GetRemoteAddress())
	
	for {
		c.connection.Listen()
	}
}

func (c *Client) Close() {
	c.connection.Close()
}

func (c *Client) VersionCheckedDataReceived(data interface{}, from *net.UDPAddr) {
	if versionCheckedData, ok := data.(communication.VersionCheckedData); ok {
		fmt.Println("Recv VersionCheckedData:", versionCheckedData, "from:", from)
	}
}

func (c *Client) SendVersionData(data *communication.VersionData, to *net.UDPAddr) {
	c.connection.Send(data, to, communication.UDP)
	fmt.Println("Send VersionData:", *data, "to:", to)
}
