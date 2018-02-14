package server

import "fmt"
import "net"
import "log"
import "github.com/lemunozm/ASCIIArena/common"
import "github.com/lemunozm/ASCIIArena/common/communication"

type Server struct {	
	network communication.NetworkManager
}

func NewServer() *Server {
	s := &Server{}
	return s
}

func (s *Server) Run(port uint) {
	listening, err := net.Listen("tcp", ":"+port)
	if err != nil {
		 log.Panic("Connection error: ", err)
	}
	defer listening.Close()
	fmt.Printf("Server listening on: %d\n", port)

	for {
		tcpSocket, err := listening.Accept()
		if err!= nil {
			 log.Panic("Connection error: ", err)
		}
	    connection := communication.NewConnection(tcpSocket)
	    connection.RegisterReceiverData(communication.VersionData{}, s.VersionDataReceived)
	    connection.RegisterReceiverData(communication.LogInData{}, s.LogInDataaReceived)
		go connection.ListenLoop()
	}
}

func (s *Server) VersionDataReceived(data interface{}, connection *communication.Connection) {
	if versionData, ok := data.(communication.VersionData); ok {
		fmt.Println("Recv VersionData:", versionData, "from:", from)

		versionCheckedData := communication.VersionCheckedData{common.GetVersion(), true}
		connection.Send(&logInStatusData)
	}
}

func (s *Server) LogInDataReceived(data interface{}, connection *communication.Connection) {
	if logInData, ok := data.(communication.LogInData); ok {
		fmt.Println("Recv LogInData:", logInData, "from:", from)

		//registrar al cliente en base a su Addr

		//udpConnection, err := net.Dial("udp", "host:port")
		//if err != nil {
		//	log.Panic("Connection error: ", err)
		//}
		//clientRegistry.add(udpConnection)

		logInStatusData := communication.LogInStatusData{}
		connection.Send(&logInStatusData)
	}
}
