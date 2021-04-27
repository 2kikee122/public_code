package main

import "fmt"

func main() {
	//query API for specific handle
	handles := []string{"BBCNews", "BBCSport"}

	//2 channels
	user_channel := make(chan string)
	post_channel := make(chan string) 

	for _, handle := range handles {
		go searchProfile(handle, user_channel)
		go getPosts(handle, post_channel)
	}

	//listeners for both channels
	for i :=0; i<len(handles); i++ {
		fmt.Println(<- user_channel)
	}

	for i :=0; i<len(handles); i++ {
		fmt.Println(<- post_channel)
	}
}
