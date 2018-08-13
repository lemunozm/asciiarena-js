package client

import "github.com/lemunozm/ascii-arena/internal/pkg/comm"
import "github.com/lemunozm/ascii-arena/internal/pkg/version"

import "fmt"

func InfoStage(connection *comm.Connection) int {
	fmt.Printf("--- SERVER INFO ---\n")

	gamePort := -1
	if checkVersion(connection) {
		gamePort = getServerInfo(connection)
	}

	fmt.Printf("\n\n")

	return gamePort
}

func checkVersion(connection *comm.Connection) bool {
	fmt.Printf("Client version %s\n", version.Current)
	versionMessage := comm.VersionMessage{version.Current}
	connection.Send(versionMessage)

	checkedVersionMessage := comm.CheckedVersionMessage{}
	connection.Receive(&checkedVersionMessage)

	fmt.Printf("Server version %s\n", checkedVersionMessage.Version)

	if checkedVersionMessage.Validation {
		fmt.Printf("Compatible version\n")
	} else {
		fmt.Printf("Incompatible version\n")
	}

	return checkedVersionMessage.Validation
}

func getServerInfo(connection *comm.Connection) int {
	serverInfoMessage := comm.ServerInfoMessage{}
	connection.Receive(&serverInfoMessage)

	if serverInfoMessage.CurrentPlayers == serverInfoMessage.MaxPlayers {
		fmt.Printf("Game already started")
	} else {
		fmt.Printf("Game: %d/%d players\n", serverInfoMessage.CurrentPlayers, serverInfoMessage.MaxPlayers)
	}

	return serverInfoMessage.Port
}
