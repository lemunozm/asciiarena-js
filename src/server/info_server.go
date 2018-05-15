package main

import "../common/communication"

import "net"
import "strconv"
import "log"
import "strings"

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
		log.Panic("Error resolving tcp address: ", err.Error())
	}
	listener, err := net.ListenTCP("tcp", address)
	if err != nil {
		log.Panic("Error listening from tcp: ", err.Error())
	}

	for {
		connection, err := listener.AcceptTCP()
		if err != nil {
			log.Panic("Error accepting: ", err.Error())
		}

		sameVersion := s.handleVersionRequest(connection)
		if sameVersion {
			s.sendMatchInfo(connection)
		}
	}
}

func (s *InfoServer) handleVersionRequest(connection net.Conn) bool {
	var version communication.VersionData
	communication.Receive(connection, &version)

	checkedVersion := s.checkVersion(version)

	communication.Send(connection, &checkedVersion)
	return checkedVersion.Validation
}

func (s *InfoServer) sendMatchInfo(connection net.Conn) {
	matchInfo := communication.MatchInfoData{
		s.matchServer.PlayerRegistry().CurrentPlayers(),
		s.matchServer.PlayerRegistry().MaxPlayers(),
	}

	communication.Send(connection, matchInfo)
}

func (s *InfoServer) checkVersion(versionData communication.VersionData) communication.CheckedVersionData {
	const currentVersion string = "0.1.0" //TODO: initialize externally

	significantCurrentVersion := currentVersion[:strings.LastIndex(currentVersion, ".")]
	significantClientVersion := versionData.Version[:strings.LastIndex(versionData.Version, ".")]

	validation := significantCurrentVersion == significantClientVersion

	return communication.CheckedVersionData{currentVersion, validation}
}
