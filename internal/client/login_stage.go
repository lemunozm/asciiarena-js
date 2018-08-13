package client

import "github.com/lemunozm/ascii-arena/internal/pkg/comm"
import "strings"
import "fmt"

func LogInStage(connection *comm.Connection, character byte) bool {
	fmt.Printf("--- LOGIN ---\n")
	maxPlayers := logInPlayer(connection, character)
	if maxPlayers > 0 {
		return waitingPlayers(connection, maxPlayers)
	}

	return false
}

func logInPlayer(connection *comm.Connection, character byte) int {
	fmt.Printf("Login with player %c...\n", character)

	newPlayerMessage := comm.NewPlayerMessage{character}
	connection.Send(&newPlayerMessage)

	playerLoginStatusMessage := comm.PlayerLoginStatusMessage{}
	connection.Receive(&playerLoginStatusMessage)

	switch playerLoginStatusMessage.LoginStatus {
	case comm.LOGIN_SUCCESSFUL:
		fmt.Printf("Login succesful.\n")
	case comm.LOGIN_ERR_CHARACTER_EXISTS:
		fmt.Printf("Login error: player %c already exists.\n", character)
	case comm.LOGIN_ERR_GAME_STARTED:
		fmt.Printf("Login error: game started.\n")
	}

	if playerLoginStatusMessage.LoginStatus == comm.LOGIN_SUCCESSFUL {
		return playerLoginStatusMessage.MaxPlayers
	} else {
		return 0
	}
}

func waitingPlayers(connection *comm.Connection, maxPlayers int) bool {
	currentPlayers := 0
	for currentPlayers < maxPlayers {
		playersInfoMessage := comm.PlayersInfoMessage{}
		if !connection.Receive(&playersInfoMessage) {
			return false
		}

		currentPlayers = len(playersInfoMessage.Players)

		players := string(playersInfoMessage.Players)
		players = strings.Replace(players, "", " ", -1)
		players = players[1 : len(players)-1]
		fmt.Printf("Players: (%d/%d): [%v]\n", currentPlayers, maxPlayers, players)

		if currentPlayers < maxPlayers {
			fmt.Printf("Waiting players...\n")
		}
	}

	fmt.Printf("All players ready. Initializing match...\n")
	return true
}
