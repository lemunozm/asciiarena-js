package log

import "fmt"
import "io"
import "sync"
import "os"
import "time"

type COLOR string

const (
	RESET_COLOR = COLOR("\x1B[0m")

	BLACK       = COLOR("\x1B[0;30m")
	RED_DARK    = COLOR("\x1B[0;31m")
	GREEN_DARK  = COLOR("\x1B[0;32m")
	YELLOW_DARK = COLOR("\x1B[0;33m")
	BLUE_DARK   = COLOR("\x1B[0;34m")
	PURPLE_DARK = COLOR("\x1B[0;35m")
	CYAN_DARK   = COLOR("\x1B[0;35m")
	GREY_LIGHT  = COLOR("\x1B[0;37m")
	GREY_DARK   = COLOR("\x1B[1;30m")
	RED         = COLOR("\x1B[1;31m")
	GREEN       = COLOR("\x1B[1;32m")
	YELLOW      = COLOR("\x1B[1;33m")
	BLUE        = COLOR("\x1B[1;34m")
	PURPLE      = COLOR("\x1B[1;35m")
	CYAN        = COLOR("\x1B[1;36m")
	WHITE       = COLOR("\x1B[1;37m")
)

type output struct {
	name    string
	color   COLOR
	writers []io.Writer
}

type logger struct {
	mutex          sync.Mutex
	infoOutputs    output
	warningOutputs output
	errorOutputs   output
}

var l logger

func init() {
	l.infoOutputs.name = "INFO   "
	l.infoOutputs.color = CYAN
	l.infoOutputs.writers = []io.Writer{os.Stdout}

	l.warningOutputs.name = "WARNING"
	l.warningOutputs.color = YELLOW
	l.warningOutputs.writers = []io.Writer{os.Stderr}

	l.errorOutputs.name = "ERROR  "
	l.errorOutputs.color = RED
	l.errorOutputs.writers = []io.Writer{os.Stderr}
}

func writeOutput(output output, value string) string {
	now := time.Now()
	year, month, day := now.Date()
	hour, min, sec := now.Clock()

	outputNameColored := fmt.Sprintf("%s%s%s", CYAN, output.name, RESET_COLOR)

	formatedTime := fmt.Sprintf("%02d-%02d-%02d %02d:%02d:%02d", year, month, day, hour, min, sec)
	formatedTimeColored := fmt.Sprintf("%s%s%s", GREY_LIGHT, formatedTime, RESET_COLOR)

	s := fmt.Sprintf("%s %s %s\n", formatedTimeColored, outputNameColored, value)
	for _, writer := range output.writers {
		fmt.Fprint(writer, s)
	}
	return s
}

func SetInfoOutputs(writers []io.Writer) {
	l.infoOutputs.writers = writers
}

func SetWarningOutputs(writers []io.Writer) {
	l.warningOutputs.writers = writers
}

func SetErrorOutputs(writers []io.Writer) {
	l.errorOutputs.writers = writers
}

func PrintfInfo(format string, v ...interface{}) {
	if len(l.infoOutputs.writers) != 0 {
		l.mutex.Lock()
		defer l.mutex.Unlock()

		s := fmt.Sprintf(format, v...)
		writeOutput(l.infoOutputs, s)
	}
}

func PrintfWarning(format string, v ...interface{}) {
	if len(l.warningOutputs.writers) != 0 {
		l.mutex.Lock()
		defer l.mutex.Unlock()

		s := fmt.Sprintf(format, v...)
		writeOutput(l.warningOutputs, s)
	}
}

func PrintfError(format string, v ...interface{}) {
	s := fmt.Sprintf(format, v...)
	if len(l.errorOutputs.writers) != 0 {
		l.mutex.Lock()
		defer l.mutex.Unlock()

		s = writeOutput(l.warningOutputs, s)
	}
	panic(s)
}
