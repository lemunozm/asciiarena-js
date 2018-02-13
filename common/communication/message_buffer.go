package communication

import "encoding/gob"
import "bytes"
import "log"

type MessageBuffer struct {
    buffer []byte
    enc *gob.Encoder
    dec *gob.Decoder
}

type dataWrapper struct {
    Data interface{}
}

func NewMessageBuffer(size int) *MessageBuffer {
    registerMessageTypes()
    gob.Register(dataWrapper{})
    buffer := make([]byte, size)
    buffer2 := bytes.NewBuffer(buffer)
    return &MessageBuffer{buffer, gob.NewEncoder(buffer2), gob.NewDecoder(buffer2)}
}

func (m *MessageBuffer) Serialize(object interface{}){
    var wrapper dataWrapper
    wrapper.Data = object
    err := m.enc.Encode(wrapper)
    if err != nil {
        log.Panic("Encode error: ", err)
    }
}

func (m *MessageBuffer) Deserialize() interface{}{
    var wrapper dataWrapper
    err := m.dec.Decode(&wrapper)
    if err != nil {
        log.Panic("Decode error: ", err)
    }

    return wrapper.Data
}

func (m *MessageBuffer) GetBuffer() []byte {
    return m.buffer[]
}