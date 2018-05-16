package communication

import "net"
import "log"
import "fmt"
import "strings"
import "encoding/gob"

type Connection struct {
	socket net.Conn
	enc    *gob.Encoder
	dec    *gob.Decoder
}

func NewConnection(socket net.Conn) *Connection {
	registerSerializationTypes()
	c := &Connection{}
	c.socket = socket
	c.enc = gob.NewEncoder(socket)
	c.dec = gob.NewDecoder(socket)

	if true {
		fmt.Printf("Connected by %s on: %s\n", socket.RemoteAddr().Network(), socket.RemoteAddr().String())
	}
	return c
}

func (c *Connection) Send(data interface{}) {
	err := c.enc.Encode(data)
	if err != nil {
		log.Panic("Encode error: ", err)
	}

	if true {
		to := c.socket.RemoteAddr().String()
		dataType := strings.Split(fmt.Sprintf("%T", data), ".")[1]
		fmt.Printf("Send to   %s: %s: %v\n", to, dataType, data)
	}
}

func (c *Connection) Receive(data interface{}) {
	err := c.dec.Decode(data)
	if err != nil {
		log.Panic("Decode error: ", err)
	}

	if true {
		from := c.socket.RemoteAddr().String()
		dataType := strings.Split(fmt.Sprintf("%T", data), ".")[1]
		fmt.Printf("Recv from %s: %s: %v\n", from, dataType, data)
	}
}

func (c *Connection) GetSocket() net.Conn {
	return c.socket
}