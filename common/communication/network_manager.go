package communication

import "net"
import "reflect"
import "log"
import "fmt"
import "gob"

var bufferSize int = 16384

type OnDataReceived func(interface{}, *net.Conn)

type NetworkManager struct {
	callbacks         map[reflect.Type]OnDataReceived
    enc *gob.Encoder
    dec *gob.Decoder
}

func NetworkManager() NetworkManager {
    registerSerializationTypes()
    n := NetworkManager{}
    n.callbacks = map[reflect.Type]OnDataReceived{}
    n.enc = gob.NewEncoder()
    n.dec = gob.NewDecoder()
}

func (n *NetworkManager) RegisterReceiverData(data interface{}, callback OnDataReceived) {
	n.callbacks[reflect.TypeOf(data)] = callback
}

func (n *NetworkManager) Send(data interface{}, connection *net.Conn) {
    n.Encoder
}

func (n *NetworkManager) Receive(connection *net.Conn) data interface{} {
    
}


func (n *NetworkManager) ListenConnection(connection *net.Conn) {
	for {
        data := Receive(connection)
        n.callbacks[reflect.TypeOf(data)](data, connection)
    }
}


