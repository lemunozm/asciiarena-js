package common

import "encoding/gob"

type ReaderCallback func(Deserializable)

type Data struct {
	object interface{}
}

type VersionData struct {
	Version string
}

type VersionCheckedData struct {
	version    string
	Validation bool
}

type LogInData struct {
	Player int8
}

type LogInStatus uint8

const (
	LOG_IN_STATUS_OK LogInStatus = iota
	LOG_IN_STATUS_PLAYER_ALREADY_EXISTS
	LOG_IN_STATUS_PLAYER_LIMIT_REACHED
)

type LogInStatusData struct {
	LogInStatus       LogInStatus
	RequiredPlayers   uint32
	RegisteredPlayers []int8
}

type PlayerConnectionData struct {
	ConnectionState bool
	Player          int8
}

type MapData struct {
	Width  uint32
	Height uint32
	Data   []uint8
	Seed   uint32
}

type LoadMatchData struct {
	MillisecondsToStart uint32
	MapData             MapData
}

func read(dec *gob.Decoder, callback ReaderCallback) {
	var data Deserializable
	err := dec.Decode(data)
	if err != nil {
		log.Fatal("decode: ", err)
	}
	callback(data)
}
