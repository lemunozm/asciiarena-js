package communication

import "net"
import "encoding/gob"
import "../log"

// print message function

func Send(connection net.Conn, data interface{}) {
	encoder := gob.NewEncoder(connection)
	err := encoder.Encode(data)
	if err != nil {
		log.PrintfError("Encode error: ", err)
	}

	log.PrintfInfo("%s[%s]%s %sto: %s%s", log.YELLOW, data, log.RESET_COLOR, log.PURPLE, connection.RemoteAddr().String(), log.RESET_COLOR)
}

func Receive(connection net.Conn, data interface{}) {
	decoder := gob.NewDecoder(connection)
	err := decoder.Decode(data)
	if err != nil {
		log.PrintfError("Decode error: ", err)
	}

	log.PrintfInfo("%s[%s]%s %sfrom: %s%s", log.BLUE, data, log.RESET_COLOR, log.PURPLE, connection.RemoteAddr().String(), log.RESET_COLOR)

}
