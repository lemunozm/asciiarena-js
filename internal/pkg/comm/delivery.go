package comm

import "github.com/lemunozm/ascii-arena/internal/pkg/logger"

import "net"
import "encoding/gob"

type Connection struct {
	connection net.Conn
	encoder    *gob.Encoder
	decoder    *gob.Decoder
}

func NewConnection(connection net.Conn) *Connection {
	c := &Connection{
		connection: connection,
		encoder:    gob.NewEncoder(connection),
		decoder:    gob.NewDecoder(connection),
	}
	return c
}

func (c Connection) RemoteAddr() net.Addr {
	return c.connection.RemoteAddr()
}

func (c *Connection) Send(message interface{}) bool {
	err := c.encoder.Encode(message)
	if err != nil {
		logger.PrintfError("Sending to: %s%s%s => %s", logger.PURPLE, c.RemoteAddr().String(), logger.RESET_COLOR, err.Error())
	} else {
		logger.PrintfInfo("%s[%s]%s to: %s%s%s", logger.YELLOW, message, logger.RESET_COLOR, logger.PURPLE, c.RemoteAddr().String(), logger.RESET_COLOR)
	}

	return err == nil
}

func (c *Connection) Receive(message interface{}) bool {
	err := c.decoder.Decode(message)
	if err != nil {
		logger.PrintfError("Receiving from: %s%s%s => %s", logger.PURPLE, c.RemoteAddr().String(), logger.RESET_COLOR, err.Error())
	} else {
		logger.PrintfInfo("%s[%s]%s from: %s%s%s", logger.BLUE, message, logger.RESET_COLOR, logger.PURPLE, c.RemoteAddr().String(), logger.RESET_COLOR)
	}

	return err == nil
}

func (c *Connection) Close() {
	c.connection.Close()
}
