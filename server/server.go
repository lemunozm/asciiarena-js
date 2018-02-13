package server

import "fmt"
import "net"
import "github.com/lemunozm/ASCIIArena/common"
import "github.com/lemunozm/ASCIIArena/common/communication"

type Server struct {
	connection *communication.Connection
}

func NewServer(port uint) *Server {
	fmt.Printf("Server listening on: %d\n", port)

	connection := communication.NewServerConnection(port)
	return &Server{connection}
}

func (s *Server) Run() {
	s.connection.RegisterReceiverData(communication.VersionData{}, s.VersionDataReceived)

	for {
		s.connection.Listen()
	}
}

func (s *Server) Close() {
	s.connection.Close()
}

func (s *Server) VersionDataReceived(data interface{}, from *net.UDPAddr) {
	if versionData, ok := data.(communication.VersionData); ok {
		fmt.Println("Recv VersionData:", versionData, "from:", from)

		versionCheckedData := communication.VersionCheckedData{common.GetVersion(), true}
		s.SendVersionCheckedData(&versionCheckedData, from)
	}
}

func (s *Server) SendVersionCheckedData(data *communication.VersionCheckedData, to *net.UDPAddr) {
	s.connection.Send(data, to)
	fmt.Println("Send VersionCheckedData:", *data, "to:", to)
}

func (s *Server) SendState(data* communication.State) {
	s.udpConnection.Send(data, to)
}
