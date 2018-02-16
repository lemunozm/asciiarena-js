package communication

import "net"
import "reflect"
import "log"
import "fmt"
import "encoding/gob"

type Connection struct {
	socket    net.Conn
	callbacks map[reflect.Type]OnDataReceived
	enc       *gob.Encoder
	dec       *gob.Decoder
	verbose   bool
}

type dataWrapper struct {
	Data interface{}
}

type OnDataReceived func(interface{}, *Connection)

func NewConnection(socket net.Conn, verbose bool) *Connection {
	registerSerializationTypes()
	gob.Register(dataWrapper{})
	c := &Connection{}
	c.socket = socket
	c.callbacks = map[reflect.Type]OnDataReceived{}
	c.enc = gob.NewEncoder(socket)
	c.dec = gob.NewDecoder(socket)
	c.verbose = verbose

	if c.verbose {
		fmt.Printf("Connected by %s on: %s:%d\n", socket.RemoteAddr().Network(), socket.RemoteAddr().String())
	}
	return c
}

func (c *Connection) RegisterRecvData(data interface{}, callback OnDataReceived) {
	c.callbacks[reflect.TypeOf(data)] = callback
}

func (c *Connection) Send(data interface{}) {
	var wrapper dataWrapper
	wrapper.Data = data
	err := c.enc.Encode(wrapper)
	if err != nil {
		log.Panic("Encode error: ", err)
	}

	if c.verbose {
		to := c.socket.RemoteAddr().String()
		fmt.Printf("Send %T: %s from: %s\n", wrapper.Data, wrapper.Data, to)
	}
}

func (c *Connection) Receive() interface{} {
	var wrapper dataWrapper
	err := c.dec.Decode(&wrapper)
	if err != nil {
		log.Panic("Decode error: ", err)
	}

	if c.verbose {
		from := c.socket.RemoteAddr().String()
		fmt.Printf("Recv %T: %s from: %s\n", wrapper.Data, wrapper.Data, from)
	}

	return wrapper.Data
}

func (c *Connection) ListenLoop() {
	for {
		data := c.Receive()
		c.callbacks[reflect.TypeOf(data)](data, c)
	}
}

func (c *Connection) GetSocket() net.Conn {
	return c.socket
}
