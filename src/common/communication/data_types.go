package communication

import "fmt"

type VersionData struct {
	Version string
}

func (d VersionData) String() string {
	return fmt.Sprintf("%s | %s", "VERSION", d.Version)
}

type CheckedVersionData struct {
	Version    string
	Validation bool
}

func (d CheckedVersionData) String() string {
	return fmt.Sprintf("%s | %s | %t", "CHECKED_VERSION", d.Version, d.Validation)
}

type ServerInfoData struct {
	Port           int
	CurrentPlayers int
	MaxPlayers     int
}

func (d ServerInfoData) String() string {
	return fmt.Sprintf("%s | %d | %d | %d", "SERVER_INFO", d.Port, d.CurrentPlayers, d.MaxPlayers)
}
