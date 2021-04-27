import pandas as pd
from youtube_api import YouTubeDataAPI
import time
from sqlalchemy import create_engine
import pymysql
from datetime import datetime

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

api_key = 'xxx'
yt = YouTubeDataAPI(api_key)

#GET HANDLES TO QUERY
db_connection_str = 'mysql+pymysql://app:xxx^%gv$$@localhost/sotrics'
db_connection = create_engine(db_connection_str)

#SELECT DISTINCT INCASE
df = pd.read_sql('SELECT distinct handle FROM yt_users', con=db_connection)

li = df['handle'].tolist()

for handle in li:
  try:
    #configure API credentials

    #Extract channel meta data - extract multiple user data by passing list.
    channel_meta = yt.get_channel_metadata(str(handle))
    channel = pd.DataFrame(channel_meta, index=[0])

    #From that channel, take the playlist_id_uploads and extract all the videos
    channelID = channel['playlist_id_uploads'].values[0]
    all_videos = yt.get_videos_from_playlist_id(channelID) #UUvlJkDfgfG3J38pup6lvrPg
    videos_list = pd.DataFrame(all_videos)

    def convert_time(row):
      new_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(row['publish_date']))
      return new_time

    videos_list.reset_index()

    #convert epoch to timestamp
    videos_list['time_pub'] = videos_list.apply(convert_time, axis = 1)

    #Extract video ID's to a list
    videos = videos_list['video_id'].tolist()

    #Extract all the video metadata to a dataframe
    query = yt.get_video_metadata(videos)
    vids = pd.DataFrame(query)

    #Sum colums to work out totals
    likes = pd.to_numeric(vids['video_like_count']).sum()
    dislikes = pd.to_numeric(vids['video_dislike_count']).sum()
    comments = pd.to_numeric(vids['video_comment_count']).sum()

    #Apply those totals to columns in our original channel df
    channel['likes'] = likes
    channel['comments'] = comments
    channel['dislikes'] = dislikes

    #restrict the output to only useful columns
    channel = channel[['description',  'video_count', 'view_count', 'subscription_count', 'account_creation_date', 'title', 'channel_id', 'comments', 'likes', 'dislikes']]

    #convert epoch time to useful timestamp to work out account age
    def convert_time(row):
      new_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(row['account_creation_date'])))
      return new_time

    channel['account_creation'] = channel.apply(convert_time, axis = 1)
    channel['dt'] = nowdt2
    channel['user'] = handle
    channel.to_sql(con=db_connection_str, name='ytoverview', if_exists='append')


    db_connection_str = 'mysql+pymysql://app:xxx^%gv$$@localhost/sotrics'
    db_connection = create_engine(db_connection_str)

    vids = vids[['video_title', 'video_publish_date', 'video_view_count', 'video_comment_count', 'video_like_count', 'video_dislike_count']]

    #convert epoch time to useful timestamp
    def convert_time(row):
      vids['video_hour'] = time.strftime('%H', time.localtime(int(row['video_publish_date'])))
      date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(row['video_publish_date'])))
      return date

    def convert_time2(row):
      vids['video_hour'] = time.strftime('%H', time.localtime(int(row['video_publish_date'])))
      date = time.strftime('%Y%m%d', time.localtime(int(row['video_publish_date'])))
      return date

    def convert_time3(row):
      vids['video_hour'] = time.strftime('%H', time.localtime(int(row['video_publish_date'])))
      date = time.strftime('%Y-%m-%d', time.localtime(int(row['video_publish_date'])))
      return date

    vids['dt'] = vids.apply(convert_time2, axis = 1)
    vids['video_date'] = vids.apply(convert_time3, axis = 1)
    vids['video_datetime'] = vids.apply(convert_time, axis = 1)
    vids['user'] = handle
    vids.to_sql(con=db_connection_str, name='ytvids', if_exists='replace')

  except:
    pass