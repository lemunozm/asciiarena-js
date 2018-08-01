package server

import "github.com/lemunozm/ascii-arena/internal/pkg/logger"
import "github.com/lemunozm/ascii-arena/internal/pkg/version"
import "github.com/lemunozm/ascii-arena/internal/pkg/comm"

import "net"
import "strconv"

type InfoServer struct {
	port        int
	matchServer *MatchServer
}

func NewInfoServer(port int, matchServer *MatchServer) *InfoServer {
	s := &InfoServer{
		port:        port,
		matchServer: matchServer,
	}
	return s
}

func (s *InfoServer) Run() {
	address, err := net.ResolveTCPAddr("tcp", ":"+strconv.Itoa(s.port))
	if err != nil {
		logger.PrintfPanic("Error resolving tcp address => %s", err.Error())
	}
	listener, err := net.ListenTCP("tcp", address)
	if err != nil {
		logger.PrintfPanic("Error listening from tcp => %s", err.Error())
	}

	for {
		tcpConnection, err := listener.AcceptTCP()
		if err != nil {
			logger.PrintfPanic("Error accepting => %s", err.Error())
		}
		connection := comm.NewConnection(tcpConnection)

		compatibleVersions := s.handleVersionRequest(connection)
		if compatibleVersions {
			s.sendServerInfo(connection)
		}
	}
}

func (s *InfoServer) handleVersionRequest(connection *comm.Connection) bool {
	clientVersionMessage := comm.VersionMessage{}
	connection.Receive(&clientVersionMessage)

	var validation bool
	compatibility := version.CheckCompatibility(clientVersionMessage.Version, version.Current)
	switch compatibility {
	case version.INCOMPATIBLE:
		validation = false
		logger.PrintfError("Incompatible versions: client is %s, and server is %s", clientVersionMessage.Version, version.Current)
	case version.COMPATIBLE_WARNING:
		validation = true
		logger.PrintfError("Compatible version, but are not the same: client is %s, and server is %s", clientVersionMessage.Version, version.Current)
	case version.COMPATIBLE:
		validation = true
	}

	checkedVersionMessage := comm.CheckedVersionMessage{version.Current, validation}
	connection.Send(checkedVersionMessage)

	return checkedVersionMessage.Validation
}

func (s *InfoServer) sendServerInfo(connection *comm.Connection) {
	serverInfoMessage := comm.ServerInfoMessage{
		s.matchServer.Port(),
		s.matchServer.MatchManager().PlayerRegistry().CurrentPlayers(),
		s.matchServer.MatchManager().PlayerRegistry().MaxPlayers(),
	}

	connection.Send(serverInfoMessage)
}
