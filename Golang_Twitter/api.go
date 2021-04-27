package main

import "github.com/amit-lulla/twitterapi" //https://godoc.org/github.com/amit-lulla/twitterapi

func connect()  *twitterapi.TwitterApi {
	twitterapi.SetConsumerKey("consumerkey")
    twitterapi.SetConsumerSecret("secretkey")  
	api := twitterapi.NewTwitterApi("api", "credentials")
	return api
}