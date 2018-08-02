package version

import "strings"

const Current string = "0.1.0"

type Compatibility int

const (
	COMPATIBLE = Compatibility(iota)
	COMPATIBLE_WARNING
	INCOMPATIBLE
)

func CheckCompatibility(clientVersion string, serverVersion string) Compatibility {

	if clientVersion == serverVersion {
		return COMPATIBLE
	}

	clientRelevantVersion := clientVersion[:strings.LastIndex(clientVersion, ".")]
	serverRelevantVersion := serverVersion[:strings.LastIndex(serverVersion, ".")]

	if clientRelevantVersion == serverRelevantVersion {
		return COMPATIBLE_WARNING
	}

	return INCOMPATIBLE
}
