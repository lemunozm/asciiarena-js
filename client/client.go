package client

import "fmt"

type Client struct {
	version string
	host    string
	port    string
}

func NewClient() Client {
	return Client{}
}

func (client *Client) Run() {
	fmt.Println("Running...")
	//TODO
}
