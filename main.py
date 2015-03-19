import praw 
import settings, elections, mods
import requests, requests.auth
import json
import time
import re
from datetime import datetime, date, timedelta
from parsers import WikiParser

with open('logins.json') as l:
    logins = json.loads(l.read())


username = logins['username']
password = logins['password']
clientID = logins['clientId']
clientSecret = logins['clientSecret']
electionInstructions = ("Moderators up for election today: %s\n\n"
                       "To vote, please write a comment with only the name of the moderator you with to vote for. Spelling matters, capitalization doesn't.\n\n"
                       "**IF YOU VOTE FOR MORE THAN ONE PERSON, ONLY ONE WILL BE COUNTED\n\n"
                       "Election start: %s\n\n"
                       "Election end: %s\n\n")

nominationInstructions = ("Please nominate moderators.\n\n"
                         "You may nominate as many moderators as you like. The top %d most nominated moderators will be voted on in the next election.\n\n" 
                         "To nominate, simply write down their name. Spelling matters, capitalization doesn't. Elections begin when nominations end.\n\n"
                         "Nomination start: %s\n\n"
                         "Nomination end: %s\n\n")

requestString = r"(?i)Requested Subreddit: (.+)"

r = praw.Reddit("ElectionBot by /u/thirdegree")
parser = WikiParser(r)

#Still need to make sure this works in the wild.
def authenticate():
    client_auth = requests.auth.HTTPBasicAuth(clientID, clientSecret)
    post_data = {"grant_type":"password", "username":username, "password":password}
    time.sleep(5)
    response = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data)
    res = response.json()
    if 'access_token' in res:    
        logins['accessToken'] = res['access_token']

    access_token = logins['accessToken']

    print res
    r.set_oauth_app_info(client_id=clientID,
                        client_secret=clientSecret,
                        redirect_uri='http://127.0.0.1/')
    r.set_access_credentials(scope=set('*'), access_token=access_token)
    r.login(username, password)


def post_vote_thread(subreddit):
    subreddit = subreddit.lower()
    try:
        election = elections.get_election(subreddit)
        sub = mods.get_subreddit(subreddit)
        electionUrl = r.submit(subreddit, "%s election"%subreddit, 
                text=electionInstructions%(reduce(lambda x,y: x+", "+y, sub['nominatedMods']), 
                                            election.electionStart, 
                                            election.electionEnd))
        elections.add_election_url(subreddit, electionUrl.url)
    except KeyError as e:
        print "ERROR: Attempted to post election thread to %s, no such subreddit known."%e

def post_nomination_thread(subreddit, nominationStart=date.today(), 
                            electionStart=(date.today() + timedelta(days=7))):
    subreddit = subreddit.lower()
    try:
        election = elections.get_election(subreddit)
        sub = mods.get_subreddit(subreddit)
        nominationUrl = r.submit(subreddit, "%s nominations"%subreddit,
                text=nominationInstructions%(sub['numberOfMods'], 
                                             nominationStart,
                                             electionStart))
        elections.add_nomination_url(subreddit, nominationUrl.url)

    except KeyError as e:
        print "ERROR: Attempted to post election thread to %s, no such subreddit known."%e

def count_votes(subreddit):
    subreddit = subreddit.lower()
    try:
        election = elections.get_election(subreddit)
        url = election.electionUrl
        post = r.get_submission(url=url)
        mod = mods.get_subreddit(subreddit)
        votes = {}
        voteCount = {i:0 for i in mod['nominatedMods']}
        for comment in praw.helpers.flatten_tree(post.comments):
            votes[comment.author] = comment.body
        for k, v in votes.items():
            if v in voteCount:
                voteCount[v] += 1
        return voteCount
    except AttributeError as e:
        print "ERROR: Attempted to count votes for %s, no such subreddit known."%subreddit
        return False

def add_subreddit(subreddit, modList, nominated_mods = [], next_elec=date.today(), frequency=28, duration=7, positions=1, ):
    subreddit = subreddit.lower()
    settings.add_subreddit(subreddit, next_elec, frequency, duration, positions)
    mods.add_subreddit(subreddit, modList, nominated_mods, numberOfMods=positions)

def post_todays_nominations():
    noms = elections.get_todays_nominations()
    for nom in noms:
        if nom.nominationUrl == "":
            post_nomination_thread(nom.subreddit, nom.nominationStart, nom.electionStart)

def post_todays_elections():
    elecs = elections.get_todays_elections()
    for elec in elecs:
        if elec.electionUrl == "":
            post_vote_thread(elec.subreddit)

def get_nominated(subreddit):
    subreddit = subreddit.lower()
    election = elections.get_election(subreddit)
    url = election.nominationUrl
    thread = r.get_submission(url=url)
    nominated = {}
    how_many = settings.get_settings(subreddit).positions
    for comment in praw.helpers.flatten_tree(thread.comments):
        if comment.body.strip().lower() in nominated:
            nominated[comment.body.strip().lower()] += 1
        else:
            nominated[comment.body.strip().lower()] = 1
    #reversed returns an iterable, which list comp doesn't take kindly to.
    sortednoms = list(reversed(sorted(nominated.items(),key=lambda x:x[1])))
    top_10 = [i[0] for i in sortednoms[:how_many]]
    mods.mod_nominated(subreddit, top_10)

def get_all_nominated():
    elecs = elections.get_todays_elections()
    for elec in elecs:
        get_nominated(elec.subreddit)

def get_addition_requests():
    inbox = r.get_unread()
    for message in inbox:
        m = re.match(requestString, message.body)
        if m:
            sub = m.group(1) #first capture group is full match, second is subreddit
            #I need the parsers to get past here
            parser.get_raw_conditions(sub)
            mods = [i.name for i in r.get_moderators(sub)]
            frequency = parser.get_frequency()
            next_elec = parser.get_next_election()
            duration = parser.get_duration()
            positions = parser. get_positions()
            add_subreddit(sub, mods, frequency=frequency, duration=duration, positions=positions, next_elec=next_elec)







