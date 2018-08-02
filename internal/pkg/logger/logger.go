package logger

import "fmt"
import "io"
import "sync"
import "os"
import "time"

type Color string

const (
	RESET_COLOR = Color("\x1B[0m")

	BLACK       = Color("\x1B[0;30m")
	RED_DARK    = Color("\x1B[0;31m")
	GREEN_DARK  = Color("\x1B[0;32m")
	YELLOW_DARK = Color("\x1B[0;33m")
	BLUE_DARK   = Color("\x1B[0;34m")
	PURPLE_DARK = Color("\x1B[0;35m")
	CYAN_DARK   = Color("\x1B[0;36m")
	GREY_LIGHT  = Color("\x1B[0;37m")
	GREY_DARK   = Color("\x1B[1;30m")
	RED         = Color("\x1B[1;31m")
	GREEN       = Color("\x1B[1;32m")
	YELLOW      = Color("\x1B[1;33m")
	BLUE        = Color("\x1B[1;34m")
	PURPLE      = Color("\x1B[1;35m")
	CYAN        = Color("\x1B[1;36m")
	WHITE       = Color("\x1B[1;37m")
)

type output struct {
	name    string
	color   Color
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

	outputNameColored := fmt.Sprintf("%s%s%s", output.color, output.name, RESET_COLOR)

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
	if len(l.errorOutputs.writers) != 0 {
		l.mutex.Lock()
		defer l.mutex.Unlock()

		s := fmt.Sprintf(format, v...)
		writeOutput(l.errorOutputs, s)
	}
}

func PrintfPanic(format string, v ...interface{}) {
	s := fmt.Sprintf(format, v...)
	if len(l.errorOutputs.writers) != 0 {
		l.mutex.Lock()
		defer l.mutex.Unlock()

		writeOutput(l.errorOutputs, s)
	}
	panic(s)
}
