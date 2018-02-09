package server

import "bytes"
import "fmt"
import "log"
import "encoding/gob"
import "github.com/lemunozm/ASCIIArena/common"

type Server struct {
	port string
}

func NewServer() Server {
	return Server{}
}

type deserializable interface {
	onDeserialization()
}

func (data *common.VersionData) onDeserialization() {
	fmt.Println(data.Version)
}

func (s *Server) Run(port uint) {
	fmt.Printf("Server listening on: %d\n", port)

	var network bytes.Buffer
	gob.Register(common.VersionData{})
	enc := gob.NewEncoder(&network)

	dataOut := common.Data{&common.VersionData{"0.0.0"}}
	err := enc.Encode(dataOut)
	if err != nil {
		log.Fatal("encode:", err)
	}

	dec := gob.NewDecoder(&network)

	var dataIn common.Data
	err = dec.Decode(&data)
	if err != nil {
		log.Fatal("decode: ", err)
	}

	data.onDeserialization()
	//common.registerCallback(VersionDataReceived)
	//var logInStatusData common.LogInStatusData
	//var versionData common.VersionData
}

func (s *Server) VersionDataReceived(data *common.Serializable) {

}
