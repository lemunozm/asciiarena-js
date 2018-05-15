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

type MatchInfoData struct {
	Port           int
	CurrentPlayers int
	MaxPlayers     int
}

func (d MatchInfoData) String() string {
	return fmt.Sprintf("%s | %d | %d | %d", "MATCH_INFO", d.Port, d.CurrentPlayers, d.MaxPlayers)
}
