package communication

import "net"
import "reflect"
import "log"
import "strconv"
import "fmt"

var bufferSize int = 16384

type OnDataReceived func(interface{}, *net.UDPAddr)

type Connection struct {
	callbacks         map[reflect.Type]OnDataReceived
	messageBuffer     *MessageBuffer
	socket            *net.UDPConn
	remoteAddress *net.UDPAddr
}

func NewClientConnection(host string, tcpPort uint, udpPort) *Connection {
	localAddress, err := net.ResolveUDPAddr("udp", "127.0.0.1:0")
	if err != nil {
        log.Panic("Connection local address error: ", err)
    }

	remoteAddress, err := net.ResolveUDPAddr("udp", host+":"+strconv.FormatUint(uint64(port), 10))
	if err != nil {
        log.Panic("Connection remote address error: ", err)
    }

	socket, err := net.ListenUDP("udp", localAddress)
	if err != nil {
        log.Panic("Connection dial error: ", err)
    }
	return &Connection{map[reflect.Type]OnDataReceived{}, NewMessageBuffer(bufferSize), socket, remoteAddress} //added error
}

func NewServerConnection(port uint) *Connection {
	localAddress, err := net.ResolveUDPAddr("udp", ":"+strconv.FormatUint(uint64(port), 10))
	if err != nil {
        log.Panic("Connection local address error: ", err)
    }

	socket, err := net.ListenUDP("udp", localAddress)
	if err != nil {
        log.Panic("Connection listen error: ", err)
    }

	return &Connection{map[reflect.Type]OnDataReceived{}, NewMessageBuffer(bufferSize), socket, nil} //added error
}

func (c *Connection) RegisterReceiverData(data interface{}, callback OnDataReceived) {
	c.callbacks[reflect.TypeOf(data)] = callback
}

func (c *Connection) Send(data interface{}, to *net.UDPAddr) {
	//c.messageBuffer.Clear()
	c.messageBuffer.Serialize(data)
	_, err := c.socket.WriteToUDP(c.messageBuffer.GetBuffer(), to)
	if err != nil {
        log.Panic("Connection write error: ", err)
    }
}

func (c *Connection) Listen() {
	//c.messageBuffer.Clear()
	length, remoteAddress, err := c.socket.ReadFromUDP(c.messageBuffer.GetBuffer())
	if err != nil {
        log.Panic("Connection read error: ", err)
    }

    if(length > 0) {
    	fmt.Println(length)
    	data := c.messageBuffer.Deserialize()
		c.callbacks[reflect.TypeOf(data)](data, remoteAddress)	
    }
}

func (c *Connection) Close() {
	c.socket.Close()
}

func (c *Connection) GetRemoteAddress() *net.UDPAddr {
	return c.remoteAddress
}
