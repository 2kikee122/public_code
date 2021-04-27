package main

import "github.com/amit-lulla/twitterapi" //https://godoc.org/github.com/amit-lulla/twitterapi

func connect()  *twitterapi.TwitterApi {
        twitterapi.SetConsumerKey("x")
    twitterapi.SetConsumerSecret("x")
        api := twitterapi.NewTwitterApi("x", "x")
        return api
}
