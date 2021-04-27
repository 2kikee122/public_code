#sudo pip3 install --upgrade google-api-python-client
#Load Libraries
from oauth2client.service_account import ServiceAccountCredentials
from apiclient.discovery import build
import httplib2
import requests
import pandas as pd
import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb
from sqlalchemy import create_engine

ga_profileID = 'xxxx'

#Create service credentials
#Rename your JSON key to client_secrets.json and save it to your working folder
credentials = ServiceAccountCredentials.from_json_keyfile_name('client_secrets.json', ['https://www.googleapis.com/auth/analytics.readonly'])

#Create a service object
http = credentials.authorize(httplib2.Http())
service = build('analytics', 'v4', http=http, discoveryServiceUrl=('https://analyticsreporting.googleapis.com/$discovery/rest'))

token = credentials.get_access_token().access_token

url = 'https://www.googleapis.com/analytics/v3/data/ga?ids=ga%3A' + ga_profileID + '&start-date=30daysAgo&end-date=yesterday&metrics=ga%3Ausers%2Cga%3AbounceRate%2Cga%3AsessionDuration%2Cga%3AgoalStartsAll%2Cga%3AgoalCompletionsAll%2Cga%3AgoalConversionRateAll%2Cga%3Apageviews%2Cga%3AtimeOnPage&dimensions=ga%3Asource%2Cga%3AsocialNetwork%2Cga%3Adate&access_token=' + token
r = requests.get(url)
j = r.json()
rows = j['rows']
overview = pd.io.json.json_normalize(j)
cols = ['Source', 'Social Network', 'Date', 'Users', 'Bounce Rate', 'Session Duration', 'Goal Starts', 'Goal Completions', 'Goal Conversion Rate', 'Pageviews', 'Time on Page']
details = pd.DataFrame(rows, columns=cols)

def dt(row):
    date = row['Date']
    year = date[0:4]
    month = date[4:6]
    day = date[6:8]
    dt = year + '-' + month + '-' + day
    return dt
    
details['dt'] = details.apply(dt, axis = 1)

db_connection_str = 'mysql+pymysql://app:xxxx^%gv$$@localhost/sotrics?charset=utf8mb4'
db_connection = create_engine(db_connection_str)
details.to_sql(con=db_connection_str, name='gadetails', if_exists='append')