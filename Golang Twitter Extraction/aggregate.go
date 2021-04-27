package main

//sum the retweets for the last 100 tweets
func sumRetweets(rt_list []int) int {
        c := 0
        for _, cnt := range rt_list {
        c = c + cnt
        }
        return c
}

//Find the max retweets for the last 100 tweets
func maxRetweets(rt_list []int) int {
        c := 0
        for _, cnt := range rt_list {
        if cnt > c {
                        c = cnt
                }
        }
        return c
}

//Find the max favourites for the last 100 tweets
func maxFav(fav_list []int) int {
        c := 0
        for _, cnt := range fav_list {
        if cnt > c {
                        c = cnt
                }
        }
        return c
}

//sum the favorites for the last 100 tweets
func sumFavorites(fav_list []int) int {
        c := 0
        for _, cnt := range fav_list {
        c = c + cnt
        }
        return c
}
