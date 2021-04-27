from google_auth_oauthlib.flow import Flow
import requests

ga_profileID = 'xxxx'

# Create the flow using the client secrets file from the Google API
# Console.
flow = Flow.from_client_secrets_file(
    './secret.json',
    scopes=['https://www.googleapis.com/auth/analytics.readonly'],
    redirect_uri='urn:ietf:wg:oauth:2.0:oob')

# Tell the user to go to the authorization URL.
auth_url, _ = flow.authorization_url(prompt='consent')

print('Please go to this URL: {}'.format(auth_url))

# The user will get an authorization code. This code is used to get the
# access token.
code = input('Enter the authorization code: ')
token = flow.fetch_token(code=code)
token = token['access_token']

url = 'https://www.googleapis.com/analytics/v3/data/ga?ids=ga%3A' + ga_profileID + '&start-date=30daysAgo&end-date=yesterday&metrics=ga%3Ausers%2Cga%3AbounceRate%2Cga%3AsessionDuration%2Cga%3AgoalStartsAll%2Cga%3AgoalCompletionsAll%2Cga%3AgoalConversionRateAll%2Cga%3Apageviews%2Cga%3AtimeOnPage&dimensions=ga%3Asource%2Cga%3AsocialNetwork%2Cga%3Adate&access_token=' + token
r = requests.get(url)
j = r.json()
print(j)
