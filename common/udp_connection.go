package common

import "net"
import "reflect"

type OnDataReceived func(interface{}, *UDPAddr)

type Connection struct {
	callbacks         map[reflect.Type]OnDataReceived
	message           common.Message
	socket            *net.UDPConn
	lastRemoteAddress *net.UDPAddr
}

func NewClientConnection(host string, port uint) {
	return Connection{}
}

func NewServerConnection(port uint) {
	localAddress, err := net.ResolveUDPAddr("udp", ":"+port)
	socket, err := net.ListenUDP("udp", localAddress)
	return Connection{}
}

func (c *Connection) RegisterDataCallback(obj interface{}, callback OnDataReceived) {
	n.callbacks[reflect.TypeOf(obj)] = callback
}

func (c *Connection) DataReceived(data interface{}, from *UDPAddr) {
}

func (c *Connection) Send(data interface{}) {
	c.message.Serialize(data)
	c.socket.Write(c.message.Buffer())
}

func (c *Connection) Listen() {
	length, lastRemoteAddress, err := connection.ReadFromUDP(c.message.Buffer())
	data := c.message.Deserialize()
	n.callbacks[reflect.TypeOf(obj)](data, lastRemoteAddress)
}
