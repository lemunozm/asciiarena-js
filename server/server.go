package server

import "fmt"

type Server struct {
	port string
}

func NewServer() Server {
	return Server{}
}

func (server *Server) Run(port uint) {
	fmt.Printf("Server listening on: %d\n", port)
}
