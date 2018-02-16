package server

import "net"
import "log"
import "strconv"
import "github.com/lemunozm/ASCIIArena/common"
import "github.com/lemunozm/ASCIIArena/common/communication"

type Server struct {
	localTCPPort    string
	requiredPlayers uint
}

func NewServer(localTCPPort uint, requiredPlayers uint) *Server {
	s := &Server{}
	s.localTCPPort = strconv.FormatUint(uint64(localTCPPort), 10)
	s.requiredPlayers = requiredPlayers
	return s
}

func (s *Server) Run() {
	listening, err := net.Listen("tcp", ":"+s.localTCPPort)
	if err != nil {
		log.Panic("Connection error: ", err)
	}
	defer listening.Close()

	for {
		tcpSocket, err := listening.Accept()
		if err != nil {
			log.Panic("Connection error: ", err)
		}
		connection := communication.NewConnection(tcpSocket, true)
		connection.RegisterRecvData(communication.VersionData{}, s.RecvVersionData)
		connection.RegisterRecvData(communication.LogInData{}, s.RecvLogInData)
		go connection.ListenLoop()
	}
}

func (s *Server) RecvVersionData(data interface{}, connection *communication.Connection) {
	if versionData, ok := data.(communication.VersionData); ok {
		compatibility := common.CheckLocalVersionWith(versionData.Version) != common.VERSION_INCOMPATIBLE

		versionCheckedData := communication.VersionCheckedData{common.GetVersion(), compatibility}
		connection.Send(versionCheckedData)
	}
}

func (s *Server) RecvLogInData(data interface{}, connection *communication.Connection) {
	if _, ok := data.(communication.LogInData); ok {
		//registrar al cliente en base a su Addr

		//udpConnection, err := net.Dial("udp", "host:port")
		//if err != nil {
		//	log.Panic("Connection error: ", err)
		//}
		//clientRegistry.add(udpConnection)

		logInStatusData := communication.LogInStatusData{communication.LOG_IN_STATUS_OK, uint32(s.requiredPlayers), []int8{}}
		connection.Send(logInStatusData)
	}
}
