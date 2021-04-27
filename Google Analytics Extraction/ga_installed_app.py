import pandas as pd
import requests
from google_auth_oauthlib.flow import InstalledAppFlow


ga_profileID = 'xxxxxx' 

SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
flow = InstalledAppFlow.from_client_secrets_file('./secret.json', SCOPES)
creds = flow.run_local_server(port=0)
token = creds.token
expiry = creds.expiry

url = 'https://www.googleapis.com/analytics/v3/data/ga?ids=ga%3A' + ga_profileID + '&start-date=30daysAgo&end-date=yesterday&metrics=ga%3Ausers%2Cga%3AbounceRate%2Cga%3AsessionDuration%2Cga%3AgoalStartsAll%2Cga%3AgoalCompletionsAll%2Cga%3AgoalConversionRateAll%2Cga%3Apageviews%2Cga%3AtimeOnPage&dimensions=ga%3Asource%2Cga%3AsocialNetwork%2Cga%3Adate&access_token=' + token
r = requests.get(url)
j = r.json()
rows = j['rows']
overview = pd.io.json.json_normalize(j)
cols = ['Source', 'Social Network', 'Date', 'Users', 'Bounce Rate', 'Session Duration', 'Goal Starts', 'Goal Completions', 'Goal Conversion Rate', 'Pageviews', 'Time on Page']
details = pd.DataFrame(rows, columns=cols)


details['prev_day'] = details['Users'].shift(1)