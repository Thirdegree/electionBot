import praw
import settings
import elections
import mods
import requests
import requests.auth
import json

with open('logins.json') as l:
    logins = json.loads(l.read())


username = logins['username']
password = logins['password']
clientID = logins['clientID']
clientSecret = logins['clientSecret']
electionInstructions = "Moderators up for election today: %s\n\n"
                     + "To vote, please write a comment with only the name of the moderator you with to vote for. Spelling matters, capitalization doesn't.\n\n"
                     + "**IF YOU VOTE FOR MORE THAN ONE PERSON, NONE OF YOUR VOTES WILL BE COUNTED\n\n"
                     + "Election start: %s\n\n"
                     + "Election end: %s"
nominationInstructions = "Please nominate moderators.\n\n"
                       + "You may nominate as many moderators as you like. The top %d most nominated moderators will be voted on in the next election.\n\n" 
                       + "To nominate, simply write down their name. Spelling matters, capitalization doesn't. Elections begin when nominations end.\n\n"
                       + "Nomination start: %s\n\n"
                       + "Nomination end: %s\n\n"


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
    try:
        election = elections.get_election(subreddit)
        sub = mods.get_subreddit(subreddit)
        r.submit(subreddit, "%s election"%subreddit, 
                text=electionInstructions%(reduce(lambda x,y: x+", "+y, sub['mods']), 
                                            election[3], 
                                            election[4]))
    except KeyError as e:
        print "ERROR: Attempted to post election thread to %s, no such subreddit known."%e.message()

def post_nomination_thread(subreddit):
    try:
        election = elections.get_election(subreddit)
        sub = mods.get_subreddit(subreddit)
        r.submit(subreddit, "%s nominations"%subreddit
                text=nominationInstructions%(sub['numberOfMods'], 
                                             election[2],
                                             election[3]))
    except KeyError as e:
        print "ERROR: Attempted to post election thread to %s, no such subreddit known."%e.message()

def count_votes(subreddit):
    try:
        election = elections.get_election(subreddit)
        url = election[1]
        post = r.get_submission(url=url)
        mod = mods.get_subreddit(subreddit)
        voteCount = {i:0 for i in mod['nominatedMods']}
        for comment in praw.helpers.flatten_tree(post.comments):
            if comment.body() in voteCount:
                voteCount[comment.body()] += 1
        return voteCount
    except KeyError as e:
        print "ERROR: Attempted to count votes for %s, no such subreddit known."%e.message()
        return False

def get_nominated(subreddit):
    election

