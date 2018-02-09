package common

import "encoding/gob"
import "bytes"
import "reflect"
import "log"

type DataReceivedCallback  func (interface{})

type Message struct {
    buffer *bytes.Buffer
    enc *gob.Encoder
    dec *gob.Decoder
    callbacks map[reflect.Type]DataReceivedCallback
}

type dataWrapper struct {
    Data interface{}
}

func NewMessage(buffer *bytes.Buffer) Message {
    registerMessageTypes()
    gob.Register(dataWrapper{})
    return Message{buffer, gob.NewEncoder(buffer), gob.NewDecoder(buffer), map[reflect.Type]DataReceivedCallback{}}
}

func (m *Message) RegisterCallback(objectType interface{}, callback DataReceivedCallback) {
    m.callbacks[reflect.TypeOf(objectType)] = callback
}

func (m *Message) Write(object interface{}){
    var wrapper dataWrapper
    wrapper.Data = object
    err := m.enc.Encode(wrapper)
    if err != nil {
        log.Panic("e1: ", err)
    }
}

func (m *Message) Read(){
    var wrapper dataWrapper
    err := m.dec.Decode(&wrapper)
    if err != nil {
        log.Panic("e2: ", err)
    }

    m.callbacks[reflect.TypeOf(wrapper.Data)](wrapper.Data)
}