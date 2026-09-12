package main

import "go-web-rag/go-server/router"

func main() {
	r := router.StartRouter()
	if err := r.Run(":8080"); err != nil {
		panic(err)
	}

}
