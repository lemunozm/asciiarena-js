package server

import "bytes"
import "fmt"
import "github.com/lemunozm/ASCIIArena/common"

type Server struct {
	port string
}

func NewServer() Server {
	return Server{}
}

func (s *Server) Run(port uint) {
	fmt.Printf("Server listening on: %d\n", port)

	var network bytes.Buffer
	
	message := common.NewMessage(&network)

	versionData := common.VersionData{"0.0.0"}
	message.Write(versionData)

    message.RegisterCallback(common.VersionData{}, s.VersionDataReceived)

    message.Read()
}

func (s* Server) VersionDataReceived(data interface{}) {
	if versionData, ok := data.(common.VersionData); ok {
        fmt.Println("Post serializacion A:", versionData)
    }
    //add address to the arguments??? Implicaria que el mensaje supiese del network. Creo que mejor no, (diferencias entre cliente y servidor)
}

func (s* Server) SendVersionCheckedData(data *common.VersionCheckedData) { 
	//add address to the arguments
}