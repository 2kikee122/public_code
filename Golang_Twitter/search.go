package main

import "fmt"
import "database/sql"

type user_details struct {
	handle string
	url string
	timezone string
	StatusesCount int64
	location string
	CreatedAt string
	AccountAge float64
	FriendsCount int
	FollowersCount int
	FavouritesCount int
}
func searchProfile(profileName string, user_channel chan string) {
	api := connect()
	searchResult, _ := api.GetUsersShow(profileName, nil)
	FavouritesCount := searchResult.FavouritesCount
	FollowersCount := searchResult.FollowersCount
	FriendsCount := searchResult.FriendsCount
	CreatedAt := searchResult.CreatedAt
	Location := searchResult.Location
	StatusesCount := searchResult.StatusesCount
	TimeZone := searchResult.TimeZone
	URL := searchResult.URL
	handle := searchResult.Name
	
	acctAge := CalcAge(CreatedAt)

	output := user_details{
		handle : handle, 
		url : URL, 
		timezone: TimeZone,
		StatusesCount: StatusesCount, 
		location: Location, 
		CreatedAt: CreatedAt, 
		AccountAge: acctAge,
		FriendsCount: FriendsCount, 
		FollowersCount: FollowersCount, 
		FavouritesCount: FavouritesCount}

	fmt.Println(output)

	db, _ := sql.Open("mysql", "app:dbname^%gv$$@localhost/sotrics")
	stmt, _ := db.Prepare("insert into twgolang(handle, url, timezone, StatusesCount, location, createdat, accountage, friendscount, followercount, favcount) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)")
	//execute
	res, _ := stmt.Exec(handle, URL, TimeZone, StatusesCount, Location, CreatedAt, acctAge, FriendsCount, FollowersCount, FavouritesCount)
	// close database after all work is done

	fmt.Println(res)
	defer db.Close()

	user_channel <- "Profile Complete"
}