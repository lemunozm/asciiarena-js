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
		go s.handleConnection(connection)
	}
}

func (s *Server) handleConnection(connection *communication.Connection) {
	if s.checkVersion(connection) {
		s.logIn(connection)
		s.waitingMatch(connection)
	}
}

func (s *Server) checkVersion(connection *communication.Connection) bool {
	var versionData communication.VersionData
	connection.Receive(&versionData)

	compatibility := common.CheckLocalVersionWith(versionData.Version) != common.VERSION_INCOMPATIBLE

	versionCheckedData := communication.VersionCheckedData{common.GetVersion(), compatibility}
	connection.Send(versionCheckedData)

	return compatibility
}

func (s *Server) logIn(connection *communication.Connection) {
	var logInData communication.LogInData
	connection.Receive(&logInData)

	//registry

	logInStatusData := communication.LogInStatusData{communication.LOG_IN_STATUS_OK, uint32(s.requiredPlayers), []int8{}}
	connection.Send(logInStatusData)
}
