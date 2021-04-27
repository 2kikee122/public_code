package main

import "fmt"
import "strings"
import "net/url"
import "github.com/tobgu/qframe"
import "math"
import "github.com/tobgu/qframe/config/groupby"

func getPosts(profileName string, post_channel chan string) {
	api := connect()
	v, _ := url.ParseQuery("screen_name="+profileName+"&count=5&include_rts=False&tweet_mode=extended")
	searchResult, _ := api.GetUserTimeline(v)

	id_list := []string{}
	date_list := []string{}
	fav_list := []int{}
	rt_list := []int{}
	age_list := []float64{}
	hour_list := []string{}
	day_list := []string{}
	handle_list := []string{}
	interaction_list := []int{}
	is_max := []string{}
	is_max_fav := []string{}
	random_id := []int{}
	media := []int{}

	for _, value := range searchResult {
		id := value.IdStr
		CreatedAt := value.CreatedAt
		FavoriteCount := value.FavoriteCount
		RetweetCount := value.RetweetCount
		interactionCount := FavoriteCount+RetweetCount
	    Posted := CalcAge(CreatedAt)
		CreatedDate := CleanDate(CreatedAt)
		hour := extract_hour(CreatedAt)
        day := strings.Split(CreatedAt, " ")[0]
		rounded := math.Floor(Posted*100)/100 //rounds number
		id_list = append(id_list, id)
		date_list = append(date_list, CreatedDate)
		fav_list = append(fav_list, FavoriteCount)
		rt_list = append(rt_list, RetweetCount)
		age_list = append(age_list, rounded)
		hour_list = append(hour_list, hour)
		day_list = append(day_list, day)
		handle_list = append(handle_list, profileName)
		interaction_list = append(interaction_list, interactionCount)
		random_id = append(random_id, 1)
		media = append(media, len(value.ExtendedEntities.Media)) 

		}

		total_retweets := sumRetweets(rt_list)
		total_favorites := sumFavorites(fav_list)
		max_rt := maxRetweets(rt_list)
		max_fav := maxFav(fav_list)
		fmt.Println(total_retweets)
		fmt.Println(total_favorites)
		fmt.Println(max_rt)

	    //loop back through and assess whether that tweet has the highest retweet count
        for _, value := range searchResult {
			RetweetCount := value.RetweetCount
		    if RetweetCount == max_rt {
			    is_max = append(is_max, "YES")
		    } else {
			    is_max = append(is_max, "NO")
		    }
		}
	    //loop back through and assess whether that tweet has the highest favorite count
        for _, value := range searchResult {
			FavoriteCount := value.FavoriteCount
		    if FavoriteCount == max_fav {
			    is_max_fav = append(is_max_fav, "YES")
		    } else {
			    is_max_fav = append(is_max_fav, "NO")
		    }
		}		
		
		//Store output to a map
		f := qframe.New(map[string]interface{}{
			"media_included": media,
			"TweetID": id_list,
			"random_id": random_id,
			"Handle": handle_list,
			"CreatedAt": date_list,
			"Age": age_list,
			"FavoriteCount": fav_list,
			"FavMax": is_max_fav,
			"RetweetCount": rt_list,
			"RetweetMax": is_max,
			"interactionCount": interaction_list,
			"hour": hour_list,
			"day": day_list,
		})
		fmt.Println(f)

		datesum := func(xx []int) int {
			result := 0
			for _, x := range xx {
				result += x
			}
			return result
		}

		//aggregate for each date, sum favorites, retweets and total interactions
		g := f.GroupBy(groupby.Columns("CreatedAt")).Aggregate(qframe.Aggregation{Fn: datesum, Column: "interactionCount"}, 
				 qframe.Aggregation{Fn: datesum, Column: "RetweetCount"}, 
				 qframe.Aggregation{Fn: datesum, Column: "FavoriteCount"},
				 qframe.Aggregation{Fn: datesum, Column: "random_id"})
		fmt.Println(g)


	post_channel <- "Detailed Profile Complete"
}