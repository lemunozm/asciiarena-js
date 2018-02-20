package common

import "strings"

var version string = "0.0.0"

type VersionCompared int

const (
	VERSION_COMPATIBLE VersionCompared = iota
	VERSION_DIFFERS_BUT_COMPATIBLE
	VERSION_INCOMPATIBLE
)

func GetVersion() string {
	return version
}

func CheckLocalVersionWith(otherVersion string) VersionCompared {
	local := strings.Split(version, ".")
	other := strings.Split(otherVersion, ".")

	if local[0] == other[0] && local[1] == other[1] {
		if local[2] == other[2] {
			return VERSION_COMPATIBLE
		} else {
			return VERSION_DIFFERS_BUT_COMPATIBLE
		}
	} else {
		return VERSION_INCOMPATIBLE
	}
}
