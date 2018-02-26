package common

import "os"
import deflog "log"

type LogLevel uint64

const (
	LOG_LEVEL_NONE LogLevel = iota
	LOG_LEVEL_ERROR
	LOG_LEVEL_WARNING
	LOG_LEVEL_INFO
)

type LogType uint64

const (
	LOG_TYPE_NONE = 1 << iota
	LOG_TYPE_DEFAULT
	LOG_TYPE_MESSAGE
)

type log struct {
	Level LogLevel
	Flags LogType
	file  *os.File
}

var Log log

func ConfigureLog(filePath string) {
	Log := log{LOG_LEVEL_NONE, LOG_TYPE_NONE, os.Stdout}

	if filePath != "" {
		var err error
		Log.file, err = os.Create(filePath)
		if err != nil {
			deflog.Panic("Opening log file error: ", err)
		}
	}
}

func (l log) message() {
	// TODO
}
