package server

import "fmt"
import "net"
import "log"
import "strconv"
import "github.com/lemunozm/ASCIIArena/common"
import "github.com/lemunozm/ASCIIArena/common/communication"

type Server struct {
}

func NewServer() *Server {
	s := &Server{}
	return s
}

func (s *Server) Run(port uint) {
	listening, err := net.Listen("tcp", ":"+strconv.FormatUint(uint64(port), 10))
	if err != nil {
		log.Panic("Connection error: ", err)
	}
	defer listening.Close()
	fmt.Printf("Server listening on: %d\n", port)

	for {
		tcpSocket, err := listening.Accept()
		if err != nil {
			log.Panic("Connection error: ", err)
		}
		connection := communication.NewConnection(tcpSocket)
		connection.RegisterRecvData(communication.VersionData{}, s.RecvVersionData)
		connection.RegisterRecvData(communication.LogInData{}, s.RecvLogInData)
		go connection.ListenLoop()
	}
}

func (s *Server) RecvVersionData(data interface{}, connection *communication.Connection) {
	if versionData, ok := data.(communication.VersionData); ok {
		from := connection.GetSocket().RemoteAddr()
		fmt.Println("Recv VersionData:", versionData, "from:", from)

		versionCheckedData := communication.VersionCheckedData{common.GetVersion(), true}
		connection.Send(&versionCheckedData)
	}
}

func (s *Server) RecvLogInData(data interface{}, connection *communication.Connection) {
	if logInData, ok := data.(communication.LogInData); ok {
		from := connection.GetSocket().RemoteAddr()
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
