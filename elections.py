import sqlite3
from datetime import date, datetime, timedelta

conn = sqlite3.connect('elections.db', detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
c = conn.cursor()

class Election():
    def __init__(self, subreddit, nominationUrl, electionUrl, nominationStart, electionStart, electionEnd):
        self.subreddit = subreddit
        self.nominationUrl = nominationUrl
        self.electionUrl = electionUrl
        self.nominationStart = nominationStart
        self.electionStart = electionStart
        self.electionEnd = electionEnd

    def __str__(self):
        return self.subreddit

    __repr__ = __str__



def get_election(subreddit):
    elections = c.execute("SELECT * FROM elections WHERE subreddit=?", (subreddit,))
    ele = elections.fetchone()
    if ele:
        return Election(*ele)
    else:
        return None

def get_upcomming_elections():
    elections = c.execute("SELECT * FROM elections ORDER BY electionStart")
    return [Election(*i) for i in elections]

def get_ending_soon_elections():
    elections = c.execute("SELECT * FROM elections ORDER BY electionEnd")
    return [Election(*i) for i in elections]

def get_upcomming_nominations():
    elections = c.execute("SELECT * FROM elections ORDER BY nominationStart")

def delete_election(subreddit):
    c.execute("DELETE FROM elections WHERE subreddit=?", (subreddit,))
    conn.commit()

def prune_elections():
    c.execute("DELETE FROM elections WHERE ?>end", (str(date.today()),))
    conn.commit()

def create_election(subreddit, nominationUrl, electionUrl, nomainationStart, electionStart, electionEnd):
    c.execute("INSERT INTO elections VALUES (?, ?, ?, ?, ?, ?)", (subreddit, nominationUrl, electionUrl, nomainationStart, electionStart, electionEnd))
    conn.commit()

def add_election_url(subreddit, electionUrl):
    c.execute("UPDATE elections SET electionUrl=? WHERE subreddit=?", (electionUrl, subreddit))
    conn.commit()
