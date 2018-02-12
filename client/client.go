package client

import "fmt"
import "net"
import "github.com/lemunozm/ASCIIArena/common"

type Client struct {
	message *common.Message
}

func NewClient() Client {
	message := &common.NewMessage()

	return Client{message}
}

func (c *Client) Run(host string, port uint) {
	fmt.Printf("Connect to server on: %s:%d\n", host, port)

	localAddress, err := net.ResolveUDPAddr("udp", "127.0.0.1:0")
	remoteAddress, err := net.ResolveUDPAddr("udp", host+":"+port)
	connection, err := net.DialUDP("udp", localAddress, remoteAddress)
	defer connection.Close()

	versionData := VersionData{"0.0.0"}
	c.SendVersionData(&versionData)

	for {
		length, err := connection.Read(message.Buffer())
		data := message.Deserialize()
		networkDataCallback.give(data, remoteAddress)
	}
}

func (c *Client) VersionCheckedDataReceived(data interface{}) {
	if versionCheckedData, ok := data.(common.VersionCheckedData); ok {
		fmt.Println("Received VersionCheckedData:", versionCheckedData)
	}
}

func (c *Client) SendVersionData(data *common.VersionData) {
	message.Serialize(data)
	connection.Write(message.Buffer())
}
