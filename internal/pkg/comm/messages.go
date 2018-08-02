package comm

import "fmt"
import "strings"

// ===============================================================================
//                                VERSION MESSAGE
// ===============================================================================
type VersionMessage struct {
	Version string
}

func (m VersionMessage) String() string {
	return fmt.Sprintf("%s | %s", "VERSION", m.Version)
}

// ===============================================================================
//                           CHECKED VERSION MESSAGE
// ===============================================================================
type CheckedVersionMessage struct {
	Version    string
	Validation bool
}

func (m CheckedVersionMessage) String() string {
	return fmt.Sprintf("%s | %s | %t", "CHECKED_VERSION", m.Version, m.Validation)
}

// ===============================================================================
//                              SERVER INFO MESSAGE
// ===============================================================================
type ServerInfoMessage struct {
	Port           int
	CurrentPlayers int
	MaxPlayers     int
}

func (m ServerInfoMessage) String() string {
	return fmt.Sprintf("%s | %d | %d | %d", "SERVER_INFO", m.Port, m.CurrentPlayers, m.MaxPlayers)
}

// ===============================================================================
//                              NEW PLAYER MESSAGE
// ===============================================================================
type NewPlayerMessage struct {
	Character byte
}

func (m NewPlayerMessage) String() string {
	return fmt.Sprintf("%s | %c", "NEW_PLAYER", m.Character)
}

// ===============================================================================
//                         PLAYER LOGIN STATUS MESSAGE
// ===============================================================================

type LoginStatus int

const (
	LOGIN_SUCCESSFUL = LoginStatus(iota)
	LOGIN_ERR_FULL_PLAYERS
	LOGIN_ERR_GAME_STARTED
	LOGIN_ERR_CHARACTER_EXISTS
)

func (l LoginStatus) String() string {
	switch l {
	case LOGIN_SUCCESSFUL:
		return "SUCCESSFUL"
	case LOGIN_ERR_FULL_PLAYERS:
		return "ERROR_FULL_PLAYERS"
	case LOGIN_ERR_GAME_STARTED:
		return "ERROR_GAME_STARTED"
	case LOGIN_ERR_CHARACTER_EXISTS:
		return "ERROR_CHARACTER_EXISTS"
	default:
		return "UNKNOWN"
	}
}

type PlayerLoginStatusMessage struct {
	LoginStatus LoginStatus
}

func (m PlayerLoginStatusMessage) String() string {
	return fmt.Sprintf("%s | %v", "PLAYER_LOGIN_STATUS", m.LoginStatus)
}

// ===============================================================================
//                             PLAYERS INFO MESSAGE
// ===============================================================================

type PlayersInfoMessage struct {
	Characters []byte
}

func (m PlayersInfoMessage) String() string {
	characters := string(m.Characters)
	characters = strings.Replace(characters, "", " ", -1)
	characters = characters[1 : len(characters)-1]
	return fmt.Sprintf("%s | {%v}", "PLAYERS_INFO", characters)
}

// ===============================================================================
//                             MATCH INFO MESSAGE
// ===============================================================================

type MatchInfoMessage struct {
	Width   int
	Height  int
	MapSeed int
	MapData []byte
}

func (m MatchInfoMessage) String() string {
	return fmt.Sprintf("%s | %d | %d | %d", "MATCH_INFO", m.Width, m.MapSeed, m.MapSeed)
}
