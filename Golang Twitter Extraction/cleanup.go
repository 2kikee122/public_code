package main

import "strings"
import "time"
import "log"

func CleanDate(CreatedAt string) string {
        month := strings.Split(CreatedAt, " ")[1]
        day := strings.Split(CreatedAt, " ")[2]
        year := strings.Split(CreatedAt, " ")[5]

    if month == "Jan" {
                month = "01"
        } else if month == "Feb" {
                month = "02"
        } else if month == "Mar" {
                month = "03"
        } else if month == "Apr" {
                month = "04"
        } else if month == "May" {
                month = "05"
        } else if month == "Jun" {
                month = "06"
        } else if month == "Jul" {
                month = "07"
        } else if month == "Aug" {
                month = "08"
        } else if month == "Sep" {
                month = "09"
        } else if month == "Oct" {
                month = "10"
        } else if month == "Nov" {
                month = "11"
        } else if month == "Dec" {
                month = "12"
        }

        full_date := year + "-" + month + "-" + day

        return full_date
}

func CalcAge(CreatedAt string) float64 {
        month := strings.Split(CreatedAt, " ")[1]
        day := strings.Split(CreatedAt, " ")[2]
        year := strings.Split(CreatedAt, " ")[5]

    if month == "Jan" {
                month = "01"
        } else if month == "Feb" {
                month = "02"
        } else if month == "Mar" {
                month = "03"
        } else if month == "Apr" {
                month = "04"
        } else if month == "May" {
                month = "05"
        } else if month == "Jun" {
                month = "06"
        } else if month == "Jul" {
                month = "07"
        } else if month == "Aug" {
                month = "08"
        } else if month == "Sep" {
                month = "09"
        } else if month == "Oct" {
                month = "10"
        } else if month == "Nov" {
                month = "11"
        } else if month == "Dec" {
                month = "12"
        }

        full_date := year + "-" + month + "-" + day

        //define parsedDate as a time data type
        var parsedDate time.Time

        //convert our string datatype to be of type time
    parsedDate, err := time.Parse("2006-01-02", full_date)
    if err != nil {
        log.Fatalln(err)
    }

    today := time.Now()

        //subtract created date from today to get age
    age := today.Sub(parsedDate).Hours() / 24
        return age
}

func extract_hour(CreatedAt string) string {
        time := strings.Split(CreatedAt, " ")[3]
        hour := strings.Split(time, ":")[0]
        return hour

}
