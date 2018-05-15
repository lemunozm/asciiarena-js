package main

import "net"
import "strconv"
import "log"

type MatchServerConfiguration struct {
	TCPPort           int
	TCPPortInfo       int
	MaxPlayers        int
	PointsToWin       int
	InfoServerEnabled bool
}

type MatchServer struct {
	port           int
	pointsToWin    int
	playerRegistry *PlayerRegistry
	infoServer     *InfoServer
}

func NewMatchServer(conf MatchServerConfiguration) *MatchServer {
	s := &MatchServer{
		port:           conf.TCPPort,
		pointsToWin:    conf.PointsToWin,
		playerRegistry: NewPlayerRegistry(conf.MaxPlayers),
	}

	if conf.InfoServerEnabled {
		s.infoServer = NewInfoServer(conf.TCPPortInfo, s)
		go s.infoServer.Run()
	}

	return s
}

func (s *MatchServer) Run() {
	address, err := net.ResolveTCPAddr("tcp", ":"+strconv.Itoa(s.port))
	if err != nil {
		log.Panic("Error resolving tcp address: ", err.Error())
	}
	listener, err := net.ListenTCP("tcp", address)
	if err != nil {
		log.Panic("Error listening from tcp: ", err.Error())
	}
	defer listener.Close()

	for {
		s.waitingPlayers(listener)
		for /* anyone has points to win */ {
			s.initializingMatch()
			s.playingMatch()
		}
	}

	//s.infoServer.Close()
}

func (s *MatchServer) waitingPlayers(listener *net.TCPListener) {
	for /* Need more players for the match */ {
		_, err := listener.AcceptTCP()
		if err != nil {
			log.Panic("Error accepting: ", err.Error())
		}

		//Deserialize
		//playerRegistry.AddPlayer(connection)
	}
}

func (s *MatchServer) initializingMatch() {
	//TODO
}

func (s *MatchServer) playingMatch() {
	//TODO
}

func (s MatchServer) PlayerRegistry() *PlayerRegistry {
	return s.playerRegistry
}
