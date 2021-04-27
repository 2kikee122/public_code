package main

import (
    "fmt"
    "database/sql"
    _ "github.com/go-sql-driver/mysql"
)

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

        db, err := sql.Open("mysql", "app:xxx^%gv$$@/sotrics")
        if err != nil {
            panic(err)
        }
        // defer the close till after the main function has finished
        defer db.Close()

        // perform a db.Query insert
        st2 := fmt.Sprintf("INSERT INTO tw_overview2 VALUES ('%s','%s', %d, '%s', '%s', %f, %d, %d, %d)", handle, URL, StatusesCount, Location, CreatedAt, acctAge, FriendsCount, FollowersCount, FavouritesCount)
        fmt.Println(st2)

        // perform a db.Query insert
        insert, err := db.Query(st2)


        // if there is an error inserting, handle it
        if err != nil {
            panic(err.Error())
        }
        // be careful deferring Queries if you are using transactions
        defer insert.Close()

        user_channel <- "Profile Complete"
}
