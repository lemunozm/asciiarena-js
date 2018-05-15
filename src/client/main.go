package main

import "../common/communication"
import "../common/log"

import "net"

func main() {
	conn, err := net.Dial("tcp", "127.0.0.1:3001")
	if err != nil {
		log.PrintfError("Error at create connection", err)
	}

	version := communication.VersionData{"0.1.0"}
	communication.Send(conn, &version)

	var checkedVersion communication.CheckedVersionData
	communication.Receive(conn, &checkedVersion)
}
