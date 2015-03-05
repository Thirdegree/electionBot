#As of 2015-03-04, every function in this file works as intended.
import sqlite3
from datetime import date, datetime, timedelta

conn = sqlite3.connect('elections.db', detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
c = conn.cursor()

# this makes it easier for main to get the various variables associated with any given election.
class Election():
    def __init__(self, subreddit, nominationUrl, electionUrl, nominationStart, electionStart, electionEnd):
        self.subreddit = subreddit
        self.nominationUrl = nominationUrl
        self.electionUrl = electionUrl
        self.nominationStart = nominationStart
        self.electionStart = electionStart
        self.electionEnd = electionEnd

    def __str__(self):
        return self.subreddit + " Election"

    __repr__ = __str__ #apperently list comprehension uses __repr__ not __str__


#returns the first election for a given subreddit.
def get_election(subreddit):
    elections = c.execute("SELECT * FROM elections WHERE subreddit=?", (subreddit,))
    ele = elections.fetchone()
    if ele:
        return Election(*ele)
    else:
        return None

#returns all elections, ordered by start date. Earliest first. Maybe should only return elections that have yet to happen?
def get_upcomming_elections():
    elections = c.execute("SELECT * FROM elections ORDER BY electionStart")
    return [Election(*i) for i in elections]

#returns all elections, ordered by end date. Could differ from upcomming due to custom settings
def get_ending_soon_elections():
    elections = c.execute("SELECT * FROM elections ORDER BY electionEnd")
    return [Election(*i) for i in elections]

#returns all elections, ordered by nomination start date.
def get_upcomming_nominations():
    elections = c.execute("SELECT * FROM elections ORDER BY nominationStart")
    return [Election(*i) for i in elections]

#deleteds all elections for a given subreddit.
def delete_election(subreddit):
    c.execute("DELETE FROM elections WHERE subreddit=?", (subreddit,))
    conn.commit()

#deletes all elections that have eneded
def prune_elections():
    c.execute("DELETE FROM elections WHERE ?>electionEnd", (str(date.today()),))
    conn.commit()

def create_election(subreddit, nominationUrl, electionUrl, nomainationStart, electionStart, electionEnd):
    c.execute("INSERT INTO elections VALUES (?, ?, ?, ?, ?, ?)", (subreddit, nominationUrl, electionUrl, nomainationStart, electionStart, electionEnd))
    conn.commit()

#sepearete function because the thread isn't created for a time after the election is added to the db (thanks, nomination)
def add_election_url(subreddit, electionUrl):
    c.execute("UPDATE elections SET electionUrl=? WHERE subreddit=?", (electionUrl, subreddit))
    conn.commit()
