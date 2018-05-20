package main

import "net"

import "github.com/lemunozm/ascii-arena/pkg/communication"
import "github.com/lemunozm/ascii-arena/pkg/logger"

func main() {
	conn, err := net.Dial("tcp", "127.0.0.1:3001")
	if err != nil {
		logger.PrintfPanic("Error at create connection => %s", err.Error())
	}

	version := communication.VersionData{"0.1.0"}
	communication.Send(conn, &version)

	var checkedVersion communication.CheckedVersionData
	communication.Receive(conn, &checkedVersion)
}
