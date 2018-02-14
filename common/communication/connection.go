package communication

import "net"
import "reflect"
import "log"
import "encoding/gob"

type Connection struct {
	socket    net.Conn
	callbacks map[reflect.Type]OnDataReceived
	enc       *gob.Encoder
	dec       *gob.Decoder
}

type dataWrapper struct {
	Data interface{}
}

type OnDataReceived func(interface{}, *Connection)

func NewConnection(socket net.Conn) *Connection {
	registerSerializationTypes()
	gob.Register(dataWrapper{})
	c := &Connection{}
	c.socket = socket
	c.callbacks = map[reflect.Type]OnDataReceived{}
	c.enc = gob.NewEncoder(socket)
	c.dec = gob.NewDecoder(socket)
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
}

func (c *Connection) Receive() interface{} {
	var wrapper dataWrapper
	err := c.dec.Decode(&wrapper)
	if err != nil {
		log.Panic("Decode error: ", err)
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
