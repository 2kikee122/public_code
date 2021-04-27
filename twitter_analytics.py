from sqlalchemy import create_engine
import pymysql
import pandas as pd
import tweepy
from datetime import datetime
import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb

#Setup our comparison dates
now = datetime.now()
yday  = int(now.strftime('%s')) - 1*24*60*60
yday2  = int(now.strftime('%s')) - 30*24*60*60
profile_timecheck  = datetime.fromtimestamp(yday).strftime('%Y-%m-%d %H:%M:%S')
profile_timecheck2  = datetime.fromtimestamp(yday2).strftime('%Y-%m-%d %H:%M:%S')
mth = datetime.fromtimestamp(yday).strftime('%b')
day = datetime.fromtimestamp(yday).strftime('%d')
date_to_find = mth + ' ' + day
now_dt  = int(now.strftime('%s'))
nowdt2  = datetime.fromtimestamp(now_dt).strftime('%Y%m%d')
handle_date  = datetime.fromtimestamp(now_dt).strftime('%Y-%m-%d')

#Twitter API Auth Details
consumer_key = 'xx'
consumer_secret = 'xx'
access_token = 'xx'
access_token_secret = 'xx'
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

#truncate DB
#db= MySQLdb.connect('localhost', "app", "sotrics^%gv$$", "sotrics")
#cursor= db.cursor()
#cursor.execute("TRUNCATE TABLE twpostsx")
#db.close()

#GET HANDLES TO QUERY
db_connection_str = 'mysql+pymysql://app:xxx^%gv$$@localhost/sotrics'
db_connection = create_engine(db_connection_str)

#SELECT DISTINCT INCASE
df = pd.read_sql('SELECT distinct handle FROM handles', con=db_connection)

li = df['handle'].tolist()
i = 0
for handle in li:
  try:
    #API config applied to a variable called API for use later
    api = tweepy.API(auth)

    #create an empty dataframe
    columns = ['Date', 'Name', 'url', 'follower_count', 'friends_count', 'favourites_count', 'created_at', 'verified', 'statuses_count', 'description']
    df = pd.DataFrame(columns=columns)

    #query the API for a specific user
    test = api.get_user(handle)

    #Extract values from the output
    date = nowdt2
    name = handle #test.name
    url = test.url
    followers_count = test.followers_count
    friends_count = test.friends_count
    favourites_count = test.favourites_count
    created_at = test.created_at
    verified = test.verified
    statuses_count = test.statuses_count
    description = test.description

    #turn the output into a dictionary & convert to PD Dataframe to be appended to our empty dataframe
    output = {
      "Date": date,
      "Name": name,
      "url": url,
      "follower_count": followers_count,
      "friends_count": friends_count,
      "favourites_count": favourites_count,
      "created_at": created_at,
      "verified": verified,
      "statuses_count": statuses_count,
      "description": description,
    }

    df2 = pd.DataFrame(output, index=[0])
    df = df.append(df2)

    #Now, we will extract the latest tweets from each user and dump them into a dataframe
    tweets = api.user_timeline(screen_name = handle, count = 100, include_rts = False, tweet_mode='extended')
    json_data = [r._json for r in tweets]
    dfx = pd.io.json.json_normalize(json_data)
    maxrt = dfx['retweet_count'].max()
    maxfav = dfx['favorite_count'].max()
    df['number_retweets_yesterday'] =  dfx['retweet_count'].sum()
    df['number_favorite_yesterday'] = dfx['favorite_count'].sum()

    #Work out the account agem given the creation date
    def age(row):
      now = datetime.fromtimestamp(yday).strptime(profile_timecheck, '%Y-%m-%d %H:%M:%S')
      then = datetime.fromtimestamp(yday).strptime(str(row['created_at']), '%Y-%m-%d %H:%M:%S')
      diff = abs((now - then).days)
      return diff
    df['account_age_days'] = df.apply(age, axis = 1)

    #Find the time of the most retweeted tweet from yesterday
    most_retweeted_tweet = dfx.loc[dfx['retweet_count'] == maxrt]
    most_retweeted_tweet = most_retweeted_tweet['created_at'].values
    most_retweeted_tweet = most_retweeted_tweet[0]
    df['date_of_most_retweeted'] = most_retweeted_tweet
    most_rt_time = most_retweeted_tweet.split(' ')[3]
    most_rt_day = most_retweeted_tweet.split(' ')[0]
    df['time_of_most_retweeted'] = most_rt_time
    df['day_of_most_retweeted'] = most_rt_day
    most_favorited_tweet = dfx.loc[dfx['favorite_count'] == maxfav]
    most_favorited_tweet = most_favorited_tweet['created_at'].values
    most_favorited_tweet = most_favorited_tweet[0]
    df['date_of_most_favorited'] = most_favorited_tweet
    most_fav_time = most_favorited_tweet.split(' ')[3]
    most_fav_day = most_favorited_tweet.split(' ')[0]
    df['time_of_most_favorited'] = most_fav_time
    df['day_of_most_favorited'] = most_fav_day
    df.to_sql(con=db_connection_str, name='twoverview', if_exists='append')

    #limit output fields
    dfx = dfx[['full_text', 'created_at', 'retweet_count', 'favorite_count']]
    #extract hour from time of day
    def time_of_day(row):
      created_time = row['created_at']
      created_hour = created_time.split(' ')[3].split(':')[0]
      return created_hour

    def convert_date(row):
        date = row['created_at']
        month = date.split(' ')[1]
        if month == 'Jan':
          month = '01'
        elif month == 'Feb':
          month = '02'
        elif month == 'Mar':
          month = '03'
        elif month == 'Apr':
          month = '04'
        elif month == 'May':
          month = '05'
        elif month == 'Jun':
          month = '06'
        elif month == 'Jul':
          month = '07'
        elif month == 'Aug':
          month = '08'
        elif month == 'Sep':
          month = '09'
        elif month == 'Oct':
          month = '10'
        elif month == 'Nov':
          month = '11'
        elif month == 'Dec':
          month = '12'
        day = date.split(' ')[2]
        year = date.split(' ')[-1]
        dfx['datex']  = year+'-'+month+'-'+day
        dt = year+month+day
        return dt

    dfx['dt'] = dfx.apply(convert_date, axis = 1)

    def convert_date2(row):
        date = row['created_at']
        month = date.split(' ')[1]
        if month == 'Jan':
          month = '01'
        elif month == 'Feb':
          month = '02'
        elif month == 'Mar':
          month = '03'
        elif month == 'Apr':
          month = '04'
        elif month == 'May':
          month = '05'
        elif month == 'Jun':
          month = '06'
        elif month == 'Jul':
          month = '07'
        elif month == 'Aug':
          month = '08'
        elif month == 'Sep':
          month = '09'
        elif month == 'Oct':
          month = '10'
        elif month == 'Nov':
          month = '11'
        elif month == 'Dec':
          month = '12'
        day = date.split(' ')[2]
        year = date.split(' ')[-1]
        dt = year+'-'+month+'-'+day
        return dt

    dfx['dt2'] = dfx.apply(convert_date2, axis = 1)

    dfx['time_of_day'] = dfx.apply(time_of_day, axis = 1)
    dfx['day_of_post'] = dfx['created_at'].str.split(' ', 1).str[0]
    output = dfx[['dt', 'dt2', 'full_text', 'created_at', 'retweet_count', 'favorite_count', 'time_of_day', 'day_of_post']]
    output['name'] = handle
    print(handle)
    db_connection_str = 'mysql+pymysql://app:xxx^%gv$$@localhost/sotrics?charset=utf8mb4'
    db_connection = create_engine(db_connection_str)

    output = output[['dt2', 'name', 'dt', 'retweet_count', 'favorite_count', 'time_of_day', 'day_of_post']]
    print(output)
    if i == 0:
        output.to_sql(con=db_connection, name='twpost', if_exists='replace')
    else:
        output.to_sql(con=db_connection, name='twpost', if_exists='append')
    i = i+1

  except:
    i = i+1
    pass