package main

import "../common/communication"
import "../common/version"
import "../common/log"

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
		log.PrintfPanic("Error resolving tcp address: ", err.Error())
	}
	listener, err := net.ListenTCP("tcp", address)
	if err != nil {
		log.PrintfPanic("Error listening from tcp: ", err.Error())
	}

	for {
		connection, err := listener.AcceptTCP()
		if err != nil {
			log.PrintfPanic("Error accepting: ", err.Error())
		}

		compatibleVersions := s.handleVersionRequest(connection)
		if compatibleVersions {
			s.sendServerInfo(connection)
		}
	}
}

func (s *InfoServer) handleVersionRequest(connection net.Conn) bool {
	var clientVersion communication.VersionData
	communication.Receive(connection, &clientVersion)

	compatibility := version.CheckCompatibility(clientVersion.Version, version.Current)
	var validation bool
	switch compatibility {
	case version.INCOMPATIBLE:
		validation = false
		log.PrintfError("Incompatible versions: client is %s, and server is %s", clientVersion.Version, version.Current)
	case version.COMPATIBLE_WARNING:
		validation = true
		log.PrintfError("Compatible version, but are not the same: client is %s, and server is %s", clientVersion.Version, version.Current)
	case version.COMPATIBLE:
		validation = true
	}

	checkedVersion := communication.CheckedVersionData{version.Current, validation}
	communication.Send(connection, &checkedVersion)

	return checkedVersion.Validation
}

func (s *InfoServer) sendServerInfo(connection net.Conn) {
	serverInfo := communication.ServerInfoData{
		s.matchServer.Port(),
		s.matchServer.MatchManager().PlayerRegistry().CurrentPlayers(),
		s.matchServer.MatchManager().PlayerRegistry().MaxPlayers(),
	}

	communication.Send(connection, serverInfo)
}
