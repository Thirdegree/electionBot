import praw
import settings
import requests
import requests.auth
import json

with open('logins.json') as l:
    logins = json.loads(l.read())


username = logins['username']
password = logins['password']
clientID = logins['clientID']
clientSecret = logins['clientSecret']

r = praw.Reddit("ElectionBot by /u/thirdegree")

def authenticate():
    client_auth = requests.auth.HTTPBasicAuth(clientID, clientSecret)
    post_data = {"grant_type":"password", "username":username, "password":password}
    response = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data)
    access_token = response.json()['access_token']

    r.set_access_credentials(scope='*', access_token=access_token)

def nominations():
    pass

def post_vote_thread(subreddit):
    r.submit(subreddit, "%s election"%subreddit, text=electionInstructions)