package client

import "fmt"

type Client struct {
	host string
	port string
}

func NewClient() Client {
	return Client{}
}

func (client *Client) Run(host string, port uint) {
	fmt.Printf("Connect to server on: %s:%d\n", host, port)
}
